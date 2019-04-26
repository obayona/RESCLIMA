from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from os.path import join
from rasterLayers.models import RasterLayer
from style.models import Style
from tms.utils import getRasterImg
import traceback
import math
import tifffile as tiff
import numpy as np
from io import BytesIO
from PIL import Image
from pygeotile.tile import Tile
from osgeo import ogr, osr


MAX_ZOOM_LEVEL = 20
TILE_WIDTH     = 256
TILE_HEIGHT    = 256
R_EARTH_X = 20026376.39 #radio de la tierra en x
R_EARTH_Y = 20048966.10 #radio de la tierra en y

def root(request):
	try:
		baseURL = request.build_absolute_uri()
		xml = []
		xml.append('<?xml version="1.0" encoding="utf-8" ?>')
		xml.append('<Services>')
		xml.append('<TileMapService title="RESCLIMA TMS" ' +
		       'version="1.0" href="' + baseURL + '1.0"/>')
		xml.append('</Services>')
		return HttpResponse("\n".join(xml), content_type="text/xml")
	except:
		traceback.print_exc()
		return HttpResponse("Error")

def service(request, version):
	try:
		if version != "1.0":
			raise Http404
		baseURL = request.build_absolute_uri()
		xml = []
		xml.append('<?xml version="1.0" encoding="utf-8" ?>')
		xml.append('<TileMapService version="1.0" services="' + baseURL + '">')
		xml.append('<Title>RESCLIMA TMS</Title>')
		xml.append('<Abstract></Abstract>')
		xml.append('<TileMaps>')
		
		id = str(1)
		xml.append('<TileMap title="' + "Prect" + '"')
		xml.append('srs="EPSG:4326"')
		xml.append('href="'+baseURL+'/'+id+'"/>')
		
		xml.append('</TileMaps>')
		xml.append('</TileMapService>')
		return HttpResponse("\n".join(xml), content_type="text/xml")
	except:
		traceback.print_exc()
	return HttpResponse("Error")

def tileMap(request, version, rasterlayer_id):

	if version != "1.0":
		raise Http404

	try:
		baseURL = request.build_absolute_uri()
		xml = []
		xml.append('<?xml version="1.0" encoding="utf-8" ?>')
		xml.append('<TileMap version="1.0" ' +
		           'tilemapservice="' + baseURL + '">')
		xml.append('<Title>' + "prect" + '</Title>')
		xml.append('<Abstract></Abstract>')
		xml.append('<SRS>EPSG:4326</SRS>')
		xml.append('<BoundingBox minx="-180" miny="-90" maxx="180" maxy="90"/>')
		xml.append('<Origin x="-180" y="-90"/>')
		xml.append('<TileFormat width="' + str(TILE_WIDTH) +
		           '" height="' + str(TILE_HEIGHT) + '" ' +
		           'mime-type="image/png" extension="png"/>')
		xml.append('<TileSets profile="global-geodetic">')
		
		for zoomLevel in range(0, MAX_ZOOM_LEVEL+1):
			unitsPerPixel = _unitsPerPixel(zoomLevel)
			xml.append('<TileSet href="' + 
			           baseURL + '/' + str(zoomLevel) +
			           '" units-per-pixel="'+str(unitsPerPixel) +
			           '" order="' + str(zoomLevel) + '"/>')
		xml.append('</TileSets>')
		xml.append('</TileMap>')
		return HttpResponse("\n".join(xml), content_type="text/xml")
	except:
		traceback.print_exc()
		return HttpResponse("Error")

def pointTo3857(longitude,latitude):
	point = ogr.Geometry(ogr.wkbPoint)
	point.AddPoint(longitude, latitude)
	inSpatialRef = osr.SpatialReference()
	inSpatialRef.ImportFromEPSG(4326)

	outSpatialRef = osr.SpatialReference()
	outSpatialRef.ImportFromEPSG(3857)

	coordTransform = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)
	point.Transform(coordTransform)

	return point.GetX(), point.GetY()

def tmsTo3857(x,y,zoom):
	tile = Tile.from_tms(tms_x=x, tms_y=y, zoom=zoom)
	bounds = tile.bounds
	minLong = bounds[0].longitude
	minLat = bounds[0].latitude
	maxLong = bounds[1].longitude
	maxLat = bounds[1].latitude

	minLong,minLat = pointTo3857(minLong,minLat)
	maxLong,maxLat = pointTo3857(maxLong,maxLat)
	
	return np.array([minLong,maxLong,-maxLat,-minLat])


def getBBox(rasterlayer):
	bbox=rasterlayer.bbox
	coord4326 = SpatialReference(4326)
	coord3857 = SpatialReference(3857)
	trans = CoordTransform(coord4326, coord3857)
	bbox.transform(trans)
	coords = bbox.coords[0]
	minLong = coords[0][0]
	maxLong = coords[2][0]
	minLat = -coords[0][1]
	maxLat = -coords[2][1]
	return np.array([minLong,maxLong,maxLat,minLat])

def createImage(img):
	if (img.shape[0]!=TILE_HEIGHT or img.shape[1]!=TILE_WIDTH):
		resize_flag = True

	file = BytesIO()
	image = Image.fromarray(img)
	image.save(file, 'png')
	#file.name = 'tile.png'
	file.seek(0)
	return file

def resize(img,width,height):
	image = Image.fromarray(img)
	image = image.resize((width,height))
	return np.array(image)



def intersectRanges(a1,a2,b1,b2):
	if(a2 <= a1):
		raise Exception("Invalid range %f, %f"%(a1,a2))
	if(b2 <= b1):
		raise Exception("Invalid range %f, %f"%(b1,b2))

	c1 = max(a1,b1)
	c2 = min(a2,b2)
	if(c1>c2):
		return None,None
	return c1,c2

def intersectBBox(bbox1,bbox2):
	a1 = bbox1[0]
	a2 = bbox1[1]
	b1 = bbox2[0]
	b2 = bbox2[1]

	minLong,maxLong = intersectRanges(a1,a2,b1,b2)
	a1 = bbox1[2]
	a2 = bbox1[3]
	b1 = bbox2[2]
	b2 = bbox2[3]
	minLat,maxLat = intersectRanges(a1,a2,b1,b2)
	return np.array([minLong,maxLong,minLat,maxLat])


def createBlankTile(W,H):
	tile = np.zeros((H,W,4),dtype='uint8')
	return tile


def cropImage(raster,x1,x2,y1,y2):
	if (x1==None or x2==None or y1==None or y2==None):
		 return createBlankTile(TILE_WIDTH,TILE_HEIGHT)
	height,width,_ = raster.shape
	x1=int(round(x1));x2=int(round(x2));
	y1=int(round(y1));y2=int(round(y2));
	return raster[y1:y2,x1:x2]

#arg 831 1087 1208 256
#arg 0 80 80 256

#arg 831 1087 1208 256
#los s 831 1087 179 435

# tx1,tx2, tamano raster escalado, tamano del tile 
def calculateCropCoord(intersection_bbox,tms_bbox):
	sx1 = intersection_bbox[0]-tms_bbox[0]
	sy1 = intersection_bbox[2]-tms_bbox[2]

	sx2 = sx1 + intersection_bbox[1] - intersection_bbox[0]
	sy2 = sy1 + intersection_bbox[3] - intersection_bbox[2]

	sx1 = int(round(sx1))
	sx2 = int(round(sx2))
	sy1 = int(round(sy1))
	sy2 = int(round(sy2))
	if(sx2>TILE_WIDTH):
		sx1 = sx1 - (sx2-TILE_WIDTH)
		sx2 = TILE_WIDTH
	if(sy2>TILE_HEIGHT):
		sy1 = sy1 - (sy2-TILE_HEIGHT)
		sy2 = TILE_HEIGHT


	return sx1,sx2,sy1,sy2

def tile(request, version, rasterlayer_id, zoom, x, y):
	try:

		if version != "1.0":
			raise Http404
		#conversiones
		zoom = int(zoom);x = int(x);y = int(y)

		if zoom < 0 or zoom > MAX_ZOOM_LEVEL:
			raise Http404

		# se carga la capa
		rasterlayer = RasterLayer.objects.get(id=rasterlayer_id)
		raster = getRasterImg(rasterlayer)
		#calculos

		#bbox del tms tile
		#tms_minX, tms_maxX, tms_minY, tms_maxY 
		tms_bbox=tmsTo3857(x,y,zoom);

		# se obtiene el bbox de la capa
		ly_bbox = getBBox(rasterlayer)
		#calculos
		print("Posiciones originales")
		print("TMS box",tms_bbox)
		print("Layer box",ly_bbox)


		#Encerando coordenadas
		print("Encerando imagenes")
		translation_vector = np.array([R_EARTH_X,R_EARTH_X,R_EARTH_Y,R_EARTH_Y])
		tms_bbox = tms_bbox + translation_vector
		ly_bbox = ly_bbox + translation_vector
		print("TMS box",tms_bbox)
		print("Layer box",ly_bbox)

		print("Haciendo las coordenadas relativas a la imagen")
		minX = ly_bbox[0]
		minY = ly_bbox[2]
		translation_vector = np.array([minX,minX,minY,minY])
		tms_bbox = tms_bbox - translation_vector
		ly_bbox = ly_bbox - translation_vector

		print("TMS box",tms_bbox)
		print("Layer box",ly_bbox)
		print("---------------------------")

		# se obtiene la relacion entre el raster y el BBOX 
		pixelsHeight,pixelsWidth,_ = raster.shape
		print("H,W",pixelsHeight,pixelsWidth)
		
		fX = pixelsWidth/ly_bbox[1]
		fY = pixelsHeight/ly_bbox[3]
		print("fX",fX,"fY",fY)
		
		# tile en blanco
		tile = createBlankTile(TILE_WIDTH,TILE_HEIGHT)
		#transformar a pixeles
		scale_vector = np.array([fX,fX,fY,fY])
		tms_bbox = tms_bbox*scale_vector
		ly_bbox = ly_bbox*scale_vector
		print("Coordenadas llevadas a pixeles")
		print("TMS box",tms_bbox)
		print("Layer box",ly_bbox)
		print("Calculando area de recorte")
		intersection_bbox=intersectBBox(ly_bbox,tms_bbox)
		print("interseccion",intersection_bbox)
		
		i_minLong = intersection_bbox[0]
		i_maxLong = intersection_bbox[1]
		i_minLat = intersection_bbox[2]
		i_maxLat = intersection_bbox[3] 

		if(i_minLong==None or i_maxLong==None 
			or i_minLat==None or i_maxLat==None):
			imageData = createImage(tile)
			return HttpResponse(imageData, content_type="image/png")

		#hacer el crop
		crop_img = cropImage(raster,i_minLong,i_maxLong,i_minLat,i_maxLat)
		
		#scalar el crop al tamanio del tile
		tW = (tms_bbox[1] - tms_bbox[0])
		tH = (tms_bbox[3] - tms_bbox[2])
		tileFactorX = TILE_WIDTH/tW; tileFactorY= TILE_HEIGHT/tH;

		h,w,_ = crop_img.shape
		crop_w = int(round(w*tileFactorX))
		crop_h = int(round(h*tileFactorY))
		print("tamano del tile",crop_w,crop_h)
		crop_w = min(crop_w,TILE_WIDTH)
		crop_h = min(crop_h,TILE_HEIGHT)
		crop_img = resize(crop_img,crop_w,crop_h)
		print("tamano final del crop",crop_img.shape)

		#calcular posicion del crop en el tile
		intersection_bbox[0]=intersection_bbox[0]*tileFactorX
		intersection_bbox[2]=intersection_bbox[2]*tileFactorY
		intersection_bbox[1]=intersection_bbox[0]+crop_img.shape[1]
		intersection_bbox[3]=intersection_bbox[2]+crop_img.shape[0]

		#calcular la posicion del tile
		scale_vector = np.array([tileFactorX,tileFactorX,tileFactorY,tileFactorY])
		tms_bbox = tms_bbox*scale_vector
		print("interseccion en escala tile",intersection_bbox)
		print("tms en escala tile",tms_bbox)

		sx1,sx2,sy1,sy2 = calculateCropCoord(intersection_bbox,tms_bbox)

		print("los s",sx1,sx2,sy1,sy2)
		print(crop_img.shape,tile[sy1:sy2,sx1:sx2,:].shape)
		tile[sy1:sy2,sx1:sx2,:]=crop_img
		imageData = createImage(tile)

		return HttpResponse(imageData, content_type="image/png")

	except:
		traceback.print_exc()
		return HttpResponse("Error")

