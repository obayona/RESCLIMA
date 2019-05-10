from rasterLayers.models import RasterLayer
from style.models import Style
from style.utils import getColorMap
import tifffile as tiff
from skimage import img_as_ubyte
from os.path import join
import numpy as np

def applyStyleRaster(img,colorMap,noData):
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

	alpha = raster[:,:,3]
	alpha[img<=noData]=0

	return raster


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


def getRasterImg(rasterlayer):
	file_path = rasterlayer.file_path
	file_name = rasterlayer.file_name
	ext = rasterlayer.file_format
	file_name = file_name.replace(ext,"-proj"+ext)
	
	fullName = join(file_path,file_name)
	img = tiff.imread(fullName)

	# se obtienen los estilos
	layer_styles = Style.objects.filter(layers__id=rasterlayer.id)
	
	noData = rasterlayer.noValue
	# agregar estilo si existe
	if layer_styles.count()==1:
		layer_style = layer_styles[0]
		colorMap = getColorMap(layer_style)
		raster = applyStyleRaster(img,colorMap,noData)
	else:
		raster = scaleImage(img,noData)

	return raster

