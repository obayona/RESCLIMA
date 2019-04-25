from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from os.path import join
from rasterLayers.models import RasterLayer
from style.models import Style
from style.utils import getColorMap
import traceback
import math
import tifffile as tiff
from skimage import img_as_ubyte
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
	return minLong,maxLong,minLat,maxLat



def applyStyleRaster(img,colorMap):
	h,w = img.shape
	raster = np.zeros((h,w,4),dtype="uint8")
	
	entry = colorMap[0]
	color = entry["color"]
	color = color.replace("#","")
	rgb = list(int(color[i:i+2], 16) for i in (0, 2 ,4))
	rgb.append(255)
	quantity = entry["quantity"]
	raster[img<=quantity]=rgb

	for i,entry in enumerate(colorMap[1:-1]):
		color = entry["color"]
		color = color.replace("#","")
		rgb = list(int(color[i:i+2], 16) for i in (0, 2 ,4))
		rgb.append(255)
		quantity = entry["quantity"]
		quantity0 = colorMap[i-1]["quantity"]
		a = img>quantity0
		b = img<=quantity
		raster[np.logical_and(a,b)]= rgb


	entry = colorMap[-1]
	color = entry["color"]
	color = color.replace("#","")
	rgb = list(int(color[i:i+2], 16) for i in (0, 2 ,4))
	rgb.append(255)
	quantity = entry["quantity"]
	raster[img>quantity]=rgb

	return raster

def scaleImage(img):
	img=img_as_ubyte(img)
	h,w = img.shape
	result = np.zeros((h,w,4),dtype="uint8")
	result[:,:,0]=img
	result[:,:,1]=img
	result[:,:,2]=img
	result[:,:,3].fill(255)
	return result


def getBBox(rasterlayer):
	bbox=rasterlayer.bbox
	coord4326 = SpatialReference(4326)
	coord3857 = SpatialReference(3857)
	trans = CoordTransform(coord4326, coord3857)
	bbox.transform(trans)
	coords = bbox.coords[0]
	minX = coords[0][0]
	maxX = coords[2][0]
	minY = coords[0][1]
	maxY = coords[2][1]
	return (minX,maxX,minY,maxY)

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

def createBlankTile(W,H):
	tile = np.zeros((H,W,4),dtype='uint8')
	return tile

#Calcula la longitud del tile dependiendo del
#nivel de zoom
def getTileLength(zoomLevel,R_EARTH):
    # ancho del mundo = 2*R_EARTH
    # el numero de tiles es 2^zoomLevel
    return (2*R_EARTH)/math.pow(2,zoomLevel)


def normalizeCoord(coord,normX,normY):
	x1,x2,y1,y2 = coord
	return x1+normX,x2+normX,y1+normY,y2+normY

def cropImage(raster,x1,x2,y1,y2):
	if (x1==None or x2==None or y1==None or y2==None):
		 return createBlankTile(TILE_WIDTH,TILE_HEIGHT)
	height,width,_ = raster.shape
	x1=int(round(x1));x2=int(round(x2));
	y1=int(round(y1));y2=int(round(y2));
	return raster[y1:y2,x1:x2]


def calculateCropCoord(a1,a2,Length,tileLength):
	dif = a2 - a1
	if (a1>0 and a2<Length):
		return 0,dif
	if (a1==0):
		return tileLength-dif,tileLength
	if (a2==Length):
		return 0,dif

def tile(request, version, rasterlayer_id, zoom, x, y):
	try:
		#TODO: validar si existe la capa
		rasterlayer = RasterLayer.objects.get(id=rasterlayer_id)

		if version != "1.0":
			raise Http404
		
		zoom = int(zoom);x = int(x);y = int(y)

		if zoom < 0 or zoom > MAX_ZOOM_LEVEL:
			raise Http404

		# se carga el archivo
		file_path = rasterlayer.file_path
		file_name = rasterlayer.file_name
		ext = rasterlayer.file_format
		file_name = file_name.replace(ext,"-proj"+ext)
		fullName = join(file_path,file_name)

		img = tiff.imread(fullName)
		# se obtiene el estilo
		layer_styles = Style.objects.filter(layers__id=rasterlayer.id)
		# agregar estilo si existe
		if layer_styles.count()==1:
			layer_style = layer_styles[0]
			colorMap = getColorMap(layer_style)	
			raster = applyStyleRaster(img,colorMap)
		else:
			raster = scaleImage(img)
		#calculos

		#longitud en metros de un tile
		minLong,maxLong,minLat,maxLat=tmsTo3857(x,y,zoom);

		# se obtiene el bbox de la capa
		minX,maxX,minY,maxY = getBBox(rasterlayer)
		#calculos
		print("Posiciones originales")
		print("TMS box",minLong,maxLong,minLat,maxLat)
		print("Layer box",minX,maxX,minY,maxY)


		#Encerando coordenadas
		minX,maxX,minY,maxY = normalizeCoord((minX,maxX,minY,maxY),R_EARTH_X,R_EARTH_Y)
		minLong,maxLong,minLat,maxLat = normalizeCoord((minLong,maxLong,minLat,maxLat),R_EARTH_X,R_EARTH_Y)
		print("Emcerando imagenes")
		print("TMS box",minLong,maxLong,minLat,maxLat)
		print("Layer box",minX,maxX,minY,maxY)

		print("Haciendo las coordenadas relativas a la imagen")
		minLong,maxLong,minLat,maxLat = normalizeCoord((minLong,maxLong,minLat,maxLat),-minX,-minY)
		minX,maxX,minY,maxY = normalizeCoord((minX,maxX,minY,maxY),-minX,-minY)
		

		print("TMS box",minLong,maxLong,minLat,maxLat)
		print("Layer box",minX,maxX,minY,maxY)
		print("---------------------------")

		# se obtiene la relacion entre el raster y el BBOX 
		pixelsHeight,pixelsWidth,_ = raster.shape
		print("H,W",pixelsHeight,pixelsWidth)
		fX = pixelsWidth/maxX
		fY = pixelsHeight/maxY
		print("fX",fX,"fY",fY)
		
		#transformar a pixeles
		"""
		tms_px1 = minLong*fX
		tms_px2 = maxLong*fX
		tms_py1 = minLat*fY
		tms_py2 = maxLat*fY
		"""
		tile = createBlankTile(TILE_WIDTH,TILE_HEIGHT)
		print("Calculando area de recorte")
		tx1,tx2=intersectRanges(minX,maxX,minLong,maxLong)
		ty1,ty2=intersectRanges(minY,maxY,minLat,maxLat)
		if(tx1==None or tx2==None or ty1==None or ty2==None):
			imageData = createImage(tile)
			return HttpResponse(imageData, content_type="image/png")

		tx1 = tx1*fX; tx2 = tx2*fX;
		ty1 = ty1*fX; ty2 = ty2*fX;
		# se intercambia el eje y
		ty2 = pixelsHeight-ty2
		ty1 = pixelsHeight-ty1
		ty2,ty1 = ty1,ty2
		print("Area de recorte",tx1,tx2,ty1,ty2)

		#hacer el crop
		crop_img = cropImage(raster,tx1,tx2,ty1,ty2)

		print("tamano del crop",crop_img.shape)
		# reize a TILE SIZE

		# tile size
		tW = (maxLong - minLong)*fX
		tH = (maxLat - minLat)*fY

		

		h,w,_ = crop_img.shape
		tileFactorX = TILE_WIDTH/tW; tileFactorY= TILE_HEIGHT/tH;
		crop_w = int(round(w*tileFactorX))
		crop_h = int(round(h*tileFactorY))
		crop_w = min(crop_w,TILE_WIDTH)
		crop_h = min(crop_h,TILE_HEIGHT)
		crop_img = resize(crop_img,crop_w,crop_h)
		print("tamano final del crop",crop_img.shape)


		print("tile factor",tileFactorX,tileFactorY)
		
		tx1 = int(round(tx1*tileFactorX))
		ty1 = int(round(ty1*tileFactorY))
		tx2 = tx1 + crop_img.shape[1]
		ty2 = ty1 + crop_img.shape[0]
		print("los tx",tx1,tx2,ty1,ty2)
		pixelsHeight,pixelsWidth,_=raster.shape
		pixelsHeight = int(round(pixelsHeight*tileFactorY));
		pixelsWidth = int(round(pixelsWidth*tileFactorX))
		
		pixelsWidth = max(tx2,pixelsWidth)
		pixelsHeight = max(ty2,pixelsHeight)

		print("arg",tx1,tx2,pixelsWidth,TILE_WIDTH)
		print("arg",ty1,ty2,pixelsHeight,TILE_HEIGHT)

		sx1,sx2=calculateCropCoord(tx1,tx2,pixelsWidth,TILE_WIDTH)
		sy1,sy2=calculateCropCoord(ty1,ty2,pixelsHeight,TILE_HEIGHT)
		print("los s",sx1,sx2,sy1,sy2)
		tile[sy1:sy2,sx1:sx2,:]=crop_img
		imageData = createImage(tile)

		return HttpResponse(imageData, content_type="image/png")

	except:
		traceback.print_exc()
		return HttpResponse("Error")

