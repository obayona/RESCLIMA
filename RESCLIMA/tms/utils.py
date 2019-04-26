from rasterLayers.models import RasterLayer
from style.models import Style
from style.utils import getColorMap
import tifffile as tiff
from skimage import img_as_ubyte
from os.path import join
import numpy as np

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


def getRasterImg(rasterlayer):
	file_path = rasterlayer.file_path
	file_name = rasterlayer.file_name
	ext = rasterlayer.file_format
	file_name = file_name.replace(ext,"-proj"+ext)
	fullName = join(file_path,file_name)
	img = tiff.imread(fullName)

	# se obtienen los estilos
	layer_styles = Style.objects.filter(layers__id=rasterlayer.id)
	
	# agregar estilo si existe
	if layer_styles.count()==1:
		layer_style = layer_styles[0]
		colorMap = getColorMap(layer_style)	
		raster = applyStyleRaster(img,colorMap)
	else:
		raster = scaleImage(img)

	return raster

