# -*- encoding: utf-8 -*-

import os
from os.path import join
from RESCLIMA import settings
from models import RasterLayer
import datetime
import time
from osgeo import gdal
from osgeo import osr
from django.contrib.gis.geos import Polygon
import traceback

def get_data_date(request):
	date_text = request.POST["data_date"]
	return datetime.datetime.strptime(date_text, '%Y-%m-%d')


def getBBox(datasource):
	gt = datasource.GetGeoTransform()
	cols = datasource.RasterXSize
	rows = datasource.RasterYSize
	ext=[]
	xarr=[0,cols]
	yarr=[0,rows]

	for px in xarr:
		for py in yarr:
			x=gt[0]+(px*gt[1])+(py*gt[2])
			y=gt[3]+(px*gt[4])+(py*gt[5])
			ext.append([x,y])
			print x,y
		yarr.reverse()

	# se reproyecta a EPSG:4326
	src_srs=osr.SpatialReference()
	src_srs.ImportFromWkt(datasource.GetProjection())
	tgt_srs = osr.SpatialReference()
	tgt_srs.ImportFromEPSG(4326)

	trans_coords=[]
	transform = osr.CoordinateTransformation(src_srs,tgt_srs)
	for x,y in ext:
		x,y,z = transform.TransformPoint(x,y)
		trans_coords.append([x,y])

	minX = trans_coords[0][0]
	minY = trans_coords[1][1]
	maxX = trans_coords[2][0]
	maxY = trans_coords[0][1]

	coords = ((minX,minY),(minX,maxY),
		(maxX,maxY),(maxX,minY),(minX,minY))
	bbox = Polygon(coords)
	return bbox

def import_data(request):
	list_files = request.FILES.getlist('import_file')
	title = request.POST["title"]
	abstract = request.POST["abstract"]
	data_date = get_data_date(request)

	if (len(list_files)!=1):
		return "Se debe subir un solo archivo"

	file = list_files[0]
	# se obtiene el nombre del archivo de la capa
	fileName = file.name
	extention = fileName.split(".")[-1]
	fileName = fileName.replace("."+extention,"")
	ts = time.time()
	timestamp_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
	fileName = fileName + "-" + timestamp_str + "." + extention
	path = settings.RASTER_FILES_PATH
	fullName = join(path,fileName)

	# se guarda el archivo
	f = open(fullName,'w')
	for chunk in file.chunks():
		f.write(chunk)
	f.close()

	# se reproyecta la capa a EPSG:3857
	ext = "."+extention
	fullName_proj = fullName.replace(ext,"-proj"+ext)	
	gdal.Warp(fullName_proj,fullName, dstSRS="EPSG:3857")

	# se obtiene informacion de la capa
	datasource = gdal.Open(fullName)
	numBands = datasource.RasterCount
	srs_wkt = datasource.GetProjection()
	bbox = getBBox(datasource)

	# se guarda en la base de datos
	rasterlayer = RasterLayer()
	rasterlayer.file_path = path
	rasterlayer.file_name = fileName
	rasterlayer.file_format = extention
	# proyected
	rasterlayer.title = title
	rasterlayer.abstract = abstract
	rasterlayer.data_date = data_date
	rasterlayer.srs_wkt = srs_wkt
	rasterlayer.numBands = numBands
	rasterlayer.bbox = bbox
	rasterlayer.type = "raster";
	rasterlayer.save()
	# todo validar el formoato del archivo
	return None