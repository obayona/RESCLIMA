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
from skimage.transform import resize
from skimage import img_as_ubyte
import numpy as np
from io import BytesIO
from PIL import Image

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
	result = np.zeros((h,w,4),dtype="uint")
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
	resize_flag = False

	if (img.shape[0]!=TILE_HEIGHT or img.shape[1]!=TILE_WIDTH):
		resize_flag = True

	file = BytesIO()
	image = Image.fromarray(img)
	if(resize_flag):
		image = image.resize((TILE_WIDTH,TILE_HEIGHT))
	image.save(file, 'png')
	file.name = 'test.png'
	file.seek(0)
	return file

def intersectRanges(a1,a2,b1,b2):
	if(a2 <= a1):
		raise Exception("Invalid range %f, %f"%(a1,a2))
	if(b2 <= b1):
		raise Exception("Invalid range %f, %f"%(b1,b2))

	if(b2<a1 or b1>a2):
		return None,None
	if(b1>=a1):
		c1 = b1
	else:
		c1 = a1
	if(b2<=a2):
		c2 = b2
	else:
		c2 = a2
	return c1,c2

def calculateCropCoord(a1,a2,Length,tileLength):
	dif = a2 -a1
	if (a1>0 and a2<Length):
		return 0,dif
	if (a1==0):
		return tileLength-dif,tileLength
	if (a2==Length):
		return 0,dif

def createBlankTile(W,H):
	tile = np.zeros((W,H,4),dtype='uint8')
	return tile

#Calcula la longitud del tile dependiendo del
#nivel de zoom
def getTileLength(zoomLevel):
    # ancho del mundo = R_EARTH_X + R_EARTH_Y
    # el numero de tiles es 2^zoomLevel
    return (R_EARTH_X + R_EARTH_X)/math.pow(2,zoomLevel)


def normalizeCoord(coord,normX,normY):
	x1,x2,y1,y2 = coord
	return x1+normX,x2+normX,y1+normY,y2+normY

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
		print(fullName)
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
			tiff.imsave("imagen.tif",raster)

		#calculos
		tileLength = getTileLength(zoom)

		minLong = x*tileLength - R_EARTH_X 
		maxLong = minLong + tileLength
		minLat = y*tileLength  - R_EARTH_Y
		maxLat = minLat + tileLength
		print("Hasta aqui todo belleza")
		print("TMS box",minLong,maxLong,minLat,maxLat)
		

		# se obtiene el bbox de la capa
		minX,maxX,minY,maxY = getBBox(rasterlayer)
		print("Layer BBox:",minX,maxX,minY,maxY)
		print("---------------------------")
		print("Empiezan las transformaciones")
		#calculos
		
		#Encerando coordenadas
		print("Encerando coordenadas")
		minX,maxX,minY,maxY = normalizeCoord((minX,maxX,minY,maxY),R_EARTH_X,R_EARTH_Y)
		minLong,maxLong,minLat,maxLat = normalizeCoord((minLong,maxLong,minLat,maxLat),R_EARTH_X,R_EARTH_Y)

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
		# se obtiene el tamanio del tile en pixeles
		tW = int((maxLong - minLong)*fX)
		tH = int((maxLat - minLat)*fY)
		print(tW,tH)
		if(tH > pixelsHeight or tW> pixelsWidth):
			tile = createBlankTile(TILE_WIDTH,TILE_HEIGHT)
			imageData = createImage(tile)
			return HttpResponse(imageData, content_type="image/png")


		# se crea un tile vacio
		tile = createBlankTile(tW,tH)

		print("Calculando area de recorte")
		tx1,tx2=intersectRanges(minX,maxX,minLong,maxLong)
		ty1,ty2=intersectRanges(minY,maxY,minLat,maxLat)
		# si no hay interseccion
		if tx1==None or tx2==None or ty1==None or ty2==None:
			# se envia el tile vacio
			imageData = createImage(tile)
			return HttpResponse(imageData, content_type="image/png")


		print("Area de recorte",tx1,tx2,ty1,ty2)
		# se calcula el area de recorte en pixeles
		tx1 = int(tx1*fX);tx2 = int(tx2*fX);ty1 = int(ty1*fY);ty2 = int(ty2*fY)
		print("Area de recorte en pixeles")
		print(tx1,tx2,ty1,ty2)

		print("Area del tile en coordenadas de imagen")
		# se intercambia el eje vertical
		ty2 = pixelsHeight-ty2
		ty1 = pixelsHeight-ty1
		ty2,ty1 = ty1,ty2
		print(ty1,ty2,tx1,tx2)
		# se realiza el recorte en la imagen
		crop = raster[ty1:ty2,tx1:tx2,:]
		print(crop.shape)

		# se debe pegar en el tile el area recortada
		sx1,sx2=calculateCropCoord(tx1,tx2,pixelsWidth,tW)
		sy1,sy2=calculateCropCoord(ty1,ty2,pixelsHeight,tH)
		print(sy1,sy2,sx1,sx2)
		print(tile.shape)
		print(tile[sy1:sy2,sx1:sx2,:].shape)
		tile[sy1:sy2,sx1:sx2,:]=crop
		imageData = createImage(tile)

		return HttpResponse(imageData, content_type="image/png")

	except:
		traceback.print_exc()
		return HttpResponse("Error")

