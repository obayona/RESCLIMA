# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import shutil
import os
import datetime
from osgeo import gdal
from celery import shared_task, current_task
from .utils import getBBox
from .models import RasterLayer

@shared_task
def import_raster_layer(rasterlayer_params):
	# se obtienen los parametros de la capa
	path = rasterlayer_params["path"]
	fileName = rasterlayer_params["fileName"]
	fullName = rasterlayer_params["fullName"]
	fullName_proj = rasterlayer_params["fullName_proj"]
	extension = rasterlayer_params["extension"]
	title = rasterlayer_params["title"]
	abstract = rasterlayer_params["abstract"]
	date_str = rasterlayer_params["date_str"] # fecha como string
	data_date = datetime.datetime.strptime(date_str, '%Y-%m-%d') # fecha como objeto datetime
	categories_string = rasterlayer_params["categories_string"]

	# result del task
	result = {};

	# se actualiza el progreso
	result["error"]=None
	result["percent"]=5
	current_task.update_state(state='PROGRESS',meta=result)

	# se reproyecta la capa a EPSG:3857
	gdal.Warp(fullName_proj,fullName, dstSRS="EPSG:3857")

	# se actualiza el progreso
	result["error"]=None
	result["percent"]=20
	current_task.update_state(state='PROGRESS',meta=result)

	# se obtiene informacion de la capa
	datasource = gdal.Open(fullName)
	numBands = datasource.RasterCount
	srs_wkt = datasource.GetProjection()

	# se actualiza el progreso
	result["error"]=None
	result["percent"]=30
	current_task.update_state(state='PROGRESS',meta=result)

	# se obtiene el bbox
	bbox = getBBox(datasource)

	# se actualiza el progreso
	result["error"]=None
	result["percent"]=50
	current_task.update_state(state='PROGRESS',meta=result)


	# se guarda en la base de datos
	rasterlayer = RasterLayer()
	rasterlayer.file_path = path
	rasterlayer.file_name = fileName
	rasterlayer.file_format = extension
	# proyected
	rasterlayer.title = title
	rasterlayer.abstract = abstract
	rasterlayer.data_date = data_date
	rasterlayer.categories_string = categories_string
	rasterlayer.srs_wkt = srs_wkt
	rasterlayer.numBands = numBands
	rasterlayer.bbox = bbox
	rasterlayer.type = "raster";
	rasterlayer.save()
	
	result["error"]=None
	result["percent"]=100
	current_task.update_state(state='PROGRESS',meta=result)
	return result

