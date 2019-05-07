import numpy as np
from os.path import join, splitext
import tifffile as tiff
from rasterLayers.models import RasterLayer
from style.models import Style
from style.utils import getColorMap

#Recupera el archivo raster y lo retorna como
#una imagen con el estilo ya aplicado. 
#Es decir un numpy array de shape
# (filas, columnas, 4). Cuatro canales, rgba
#Recibe un objeto raster.RasterLayer
def getRasterImg(rasterlayer):
	file_path = rasterlayer.file_path
	file_name = rasterlayer.file_name

	parts = splitext(file_name)

	ext = parts[1]
	file_name = file_name.replace(ext,"-proj"+ext)
	
	fullName = join(file_path,file_name)
	img = tiff.imread(fullName)

	# se obtienen los estilos
	layer_styles = Style.objects.filter(layers__id=rasterlayer.id)
	# el valor de no data
	noData = rasterlayer.noValue
	numBands = rasterlayer.numBands
	# si la capa es de una banda
	if numBands==1:
		#si la capa tiene estilo
		if(layer_styles.count()==1):
			layer_style = layer_styles[0]
			colorMap = getColorMap(layer_style)
			#se crea la imagen
			raster = applyStyleRaster(img,colorMap,noData)
		else:
			#si la capa no tiene estilos
			raster = scaleImage(img,noData)
	else:
		#TODO, caso para imagenes con mas de un canal
		raster = img

	return raster

#Aplica estilo a una imagen raster de una banda
def applyStyleRaster(img,colorMap,noData):
	h,w = img.shape
	raster = np.zeros((h,w,4),dtype="uint8")
	colorMap = html2RGB(colorMap)

	N = len(colorMap)
	for i in range(0,N-1):
		entry = colorMap[i]
		entry_next = colorMap[i+1]

		quantity = entry["quantity"]
		quantity_next = entry_next["quantity"]

		rgb = entry["color"]
		rgb_next = entry_next["color"]

		a = img>=quantity
		b = img<=quantity_next
		mask = np.logical_and(a,b)
		
		result = img*mask
		result = (result - quantity)/(quantity_next-quantity)

		rgb_dif = rgb_next - rgb

		r = result*(rgb_dif[0])+rgb[0]
		g = result*(rgb_dif[1])+rgb[1]
		b = result*(rgb_dif[2])+rgb[2]
		a = np.full(shape=r.shape,fill_value=255,dtype="uint8")

		rgba = np.dstack((r,g,b,a))
		rgba = rgba.astype("uint8")
		
		raster[mask]=rgba[mask]

	return raster

#Renderiza una imagen de una banda. 
#Generalmente las rasters tienen pixels de 32 o 64 bits.
#Esta funcion transforma esa imagen a una RGBA de 8 bits.
def scaleImage(img,noData):
	#imagen sin valores noData
	img_noDataValue= img>noData
	img_notNaN = ~np.isnan(img)
	#imagen solo con valores validos
	img_notNaN = np.logical_and(img_notNaN,img_noDataValue)
	
	minValue = img[img_notNaN].min()
	maxValue = img[img_notNaN].max()

	alpha = 255.0/(maxValue - minValue)
	beta = (-minValue * 255.0)/(maxValue - minValue)

	result = alpha*img + beta
	result = np.uint8(result)

	rgb = np.zeros((result.shape[0],result.shape[1],4),dtype='uint8')
	rgb[:,:,0]=result
	rgb[:,:,1]=result
	rgb[:,:,2]=result
	rgb[:,:,3].fill(0)
	alphaC = rgb[:,:,3]
	alphaC[img_notNaN]=255

	return rgb

#convierte colores html a rgb
def html2RGB(colorMap):
	for entry in colorMap:
		color = entry["color"]
		color = color.replace("#","")
		rgb_color = list(int(color[i:i+2], 16) for i in (0, 2 ,4))
		entry["color"]=np.array(rgb_color)
		
	return colorMap

