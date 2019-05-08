from django.contrib.gis.gdal import SpatialReference, CoordTransform
from io import BytesIO
from osgeo import ogr, osr
from PIL import Image
from pygeotile.tile import Tile
from rasterLayers.models import RasterLayer
from tms.constants import *
import numpy as np
from tms.styler import getRasterImg

#tms_minX, tms_maxX, tms_minY, tms_maxY 
def renderTMS(rasterlayer,x,y,zoom):
	#se genera la imagen de la capa, ya con estilo
	raster = getRasterImg(rasterlayer)
	#Los bbox se representan como un array de 4 elementos
	#[minX,maxX,minY,maxY]
	tms_bbox=getTMSBBox(x,y,zoom);
	ly_bbox = getLayerBBox(rasterlayer)
	
	#se invierte el eje vertical de los bboxes
	tms_bbox = np.array([tms_bbox[0],tms_bbox[1],-tms_bbox[3],-tms_bbox[2]])
	ly_bbox = np.array([ly_bbox[0],ly_bbox[1],-ly_bbox[3],-ly_bbox[2]])

	#se realiza un cambio en el origen de coordenadas
	translation_vector = np.array([R_EARTH_X,R_EARTH_X,R_EARTH_Y,R_EARTH_Y])
	tms_bbox = tms_bbox + translation_vector
	ly_bbox = ly_bbox + translation_vector

	#se realiza un cambio en el origen de coordenadas, para que
	#sean relativas a la imagen
	minX = ly_bbox[0]
	minY = ly_bbox[2]
	translation_vector = np.array([minX,minX,minY,minY])
	tms_bbox = tms_bbox - translation_vector
	ly_bbox = ly_bbox - translation_vector


	# se obtiene la resolucion del pixel del raster
	pixelsHeight,pixelsWidth,_ = raster.shape	
	fX = pixelsWidth/ly_bbox[1]
	fY = pixelsHeight/ly_bbox[3]
		
	#Se crea un tile en blanco
	tile = createBlankTile(TILE_WIDTH,TILE_HEIGHT)
	
	#Las coordenadas de los bboxes se escalan a pixeles
	scale_vector = np.array([fX,fX,fY,fY])
	tms_bbox = tms_bbox*scale_vector
	ly_bbox = ly_bbox*scale_vector

	#se encuentra la interseccion entre los bboxes
	intersection_bbox=intersectBBox(ly_bbox,tms_bbox)
		
	i_minLong,i_maxLong,i_minLat,i_maxLat = intersection_bbox
	#si la inteseccion es nula se retorna el tile en blanco
	if(i_minLong==None or i_maxLong==None 
		or i_minLat==None or i_maxLat==None):
		imageData = createInMemmoryImage(tile)
		return imageData

	#Si la interseccion no es vacia se realiza el crop de la imagen
	crop_img = cropImage(raster,intersection_bbox)
	
	#Se escalala imagen recortada al tamanio del tile final	
	tW = (tms_bbox[1] - tms_bbox[0])
	tH = (tms_bbox[3] - tms_bbox[2])
	tileFactorX = TILE_WIDTH/tW; tileFactorY= TILE_HEIGHT/tH;

	h,w,_ = crop_img.shape
	#Tamanio de la imagen en el tile
	crop_w = int(round(w*tileFactorX))
	crop_h = int(round(h*tileFactorY))
	#No puede ser mayor que el tamanio final del tile	
	crop_w = min(crop_w,TILE_WIDTH)
	crop_h = min(crop_h,TILE_HEIGHT)
	#se realiza el resize
	crop_img = resizeImage(crop_img,crop_w,crop_h)

	#Se escalan las coordenadas de la interseccion al tamanio final del tile
	intersection_bbox[0]=intersection_bbox[0]*tileFactorX
	intersection_bbox[2]=intersection_bbox[2]*tileFactorY
	intersection_bbox[1]=intersection_bbox[0]+crop_img.shape[1]
	intersection_bbox[3]=intersection_bbox[2]+crop_img.shape[0]

	#Se calcula la posicion del tile
	scale_vector = np.array([tileFactorX,tileFactorX,tileFactorY,tileFactorY])
	# bbox del tms escalado al tamanio final del tile
	tms_bbox = tms_bbox*scale_vector
	
	#se obtiene la posicion final del raster recortado en el tile
	sx1,sx2,sy1,sy2 = calculateFinalPosition(intersection_bbox,tms_bbox)

	#se pega el raster recortado en el tile	
	tile[sy1:sy2,sx1:sx2,:]=crop_img
	imageData = createInMemmoryImage(tile)
	return imageData

#Recibe los tres parametros tms (x,y,zoom) y retorna
#el bbox del tile
def getTMSBBox(x,y,zoom):
	tile = Tile.from_tms(tms_x=x, tms_y=y, zoom=zoom)
	bounds = tile.bounds
	minLong = bounds[0].longitude
	minLat = bounds[0].latitude
	maxLong = bounds[1].longitude
	maxLat = bounds[1].latitude

	minLong,minLat = pointTo3857(minLong,minLat)
	maxLong,maxLat = pointTo3857(maxLong,maxLat)
	
	return np.array([minLong,maxLong,minLat,maxLat])

#Recupera el bbox de una capa raster y lo retorna en metros
# EPGS:3857
def getLayerBBox(rasterlayer):
	bbox=rasterlayer.bbox
	coord4326 = SpatialReference(4326)
	coord3857 = SpatialReference(3857)
	trans = CoordTransform(coord4326, coord3857)
	bbox.transform(trans)
	coords = bbox.coords[0]
	minLong = coords[0][0]
	maxLong = coords[2][0]
	minLat = coords[0][1]
	maxLat = coords[2][1]
	return np.array([minLong,maxLong,minLat,maxLat])


#Transforma un punto definido por longitud y latitud
# a metros, es decir EPGS:3857
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

# Crea un tile en blanco
def createBlankTile(W,H):
	tile = np.zeros((H,W,4),dtype='uint8')
	return tile


# Crea una imagen en memoria
def createInMemmoryImage(img):
	if (img.shape[0]!=TILE_HEIGHT or img.shape[1]!=TILE_WIDTH):
		resize_flag = True

	file = BytesIO()
	image = Image.fromarray(img)
	image.save(file, 'png')
	file.seek(0)
	return file

#Obtiene la interseccion entre dos bbox
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

#Obtiene la interseccion entre dos rangos numericos
# definidos por [a1,a2] y [b1,b2]
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

#Realiza Resize de una imagen al tamanio (width,heigth)
def resizeImage(img,width,height):
	image = Image.fromarray(img)
	image = image.resize((width,height))
	return np.array(image)

#Realiza el crop de una imagen
def cropImage(raster,intersection_bbox):
	col1,col2,row1,row2 = intersection_bbox

	height,width,_ = raster.shape
	col1=int(round(col1));col2=int(round(col2));
	row1=int(round(row1));row2=int(round(row2));
	return raster[row1:row2,col1:col2]

# Calcula la posicion final del crop del raster en
# el tile
def calculateFinalPosition(intersection_bbox,tms_bbox):
	sx1 = intersection_bbox[0]-tms_bbox[0]
	sy1 = intersection_bbox[2]-tms_bbox[2]

	sx2 = sx1 + intersection_bbox[1] - intersection_bbox[0]
	sy2 = sy1 + intersection_bbox[3] - intersection_bbox[2]

	sx1 = int(round(sx1))
	sx2 = int(round(sx2))
	sy1 = int(round(sy1))
	sy2 = int(round(sy2))
	#validaciones, los rangos no pueden ser mayores que
	#el tamanio del tile
	if(sx2>TILE_WIDTH):
		sx1 = sx1 - (sx2-TILE_WIDTH)
		sx2 = TILE_WIDTH
	if(sy2>TILE_HEIGHT):
		sy1 = sy1 - (sy2-TILE_HEIGHT)
		sy2 = TILE_HEIGHT

	return np.array([sx1,sx2,sy1,sy2])



