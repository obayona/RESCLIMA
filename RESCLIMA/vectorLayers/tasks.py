# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task, current_task
import time
import datetime
from django.contrib.gis.geos import Polygon
from django.db import transaction
from main.models import Researcher
from os.path import join, splitext
from osgeo import ogr
from osgeo import osr
from vectorLayers.models import VectorLayer
from RESCLIMA import settings
import json
import shutil

# modificar funciones para exportar
# probar con mas capas

@shared_task
@transaction.atomic
def import_vector_layer(vectorlayer_params):

	temp_dir = vectorlayer_params["temp_dir"]
	vectorlayer_name = vectorlayer_params["vectorlayer_name"]
	encoding  = vectorlayer_params["encoding"]
	title = vectorlayer_params["title"]
	abstract = vectorlayer_params["abstract"]
	date_str = vectorlayer_params["date_str"]
	data_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
	categories_string = vectorlayer_params["categories_string"]
	owner_id = vectorlayer_params["owner"]
	owner = Researcher.objects.get(id=owner_id)

	try:
		path = join(temp_dir,vectorlayer_name+".shp")
		datasource = ogr.Open(path)
		layer = datasource.GetLayer(0)
	except Exception as e:
		return updateResult(errorMsg = "La capa vectorial no es válida " + str(e),
			percent_progress = None)

	updateResult(errorMsg = None, percent_progress = 10)

	#se crea un geojson
	geojson = {}
	geojson["type"] = "FeatureCollection";
	geojson["crs"] = {"type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" }}
	geojson["attributes"]=[]
	geojson["features"] = []


	layer_def = layer.GetLayerDefn()
	num_fields = layer_def.GetFieldCount()
	for i in range(num_fields):
		field_def = layer_def.GetFieldDefn(i)
		attr = {}
		attr["name"]=field_def.GetName()
		attr["type"]=field_def.GetType()
		attr["width"]=field_def.GetWidth()
		attr["precision"]=field_def.GetPrecision()
		
		geojson["attributes"].append(attr)



	geometry_type = layer_def.GetGeomType() #tipo de geometria de la capa

	src_spatial_ref = layer.GetSpatialRef() #referencia espacial de la capa
	dst_spatial_ref = osr.SpatialReference()# se crea la referencia EPSG:4326
	dst_spatial_ref.ImportFromEPSG(4326)
	# se crea un objeto para transformar los sistemas de coordenadas
	# de la capa original a 4326
	coord_transform = osr.CoordinateTransformation(src_spatial_ref,dst_spatial_ref)

	# arreglos para guardar los minX, minY, maxX, maxY
	# de los features
	minXs = []; minYs = []; maxXs = []; maxYs = [];
	N = float(layer.GetFeatureCount())

	for i,feature in enumerate(layer):

		geometry = feature.GetGeometryRef()
		if(geometry==None):
			continue

		geometry.Transform(coord_transform)
		env = geometry.GetEnvelope()
		minXs.append(env[0])
		minYs.append(env[2])
		maxXs.append(env[1])
		maxYs.append(env[3])

		feature_json = feature.ExportToJson(as_object=True)
		geojson["features"].append(feature_json)

		percent_progress = 10 + (float(i)/N)*70.0
		updateResult(errorMsg = None, percent_progress = 10)


	bbox = calculateBBox(minXs, minYs, maxXs, maxYs)
	geojson["bbox"]=bbox.geojson
	
	file_path = settings.VECTOR_FILES_PATH
	file_name = createFileName(vectorlayer_name)
	full_path = join(file_path,file_name)
	f = open(full_path,"w")
	f.write(json.dumps(geojson,ensure_ascii=False))
	f.close()


	# se actualiza el progreso
	updateResult(errorMsg = None, percent_progress = 85)
	
	# se crea el objeto vectorlayer del modelo
	vectorlayer_name = vectorlayer_name.lower()
	vectorlayer = VectorLayer()
	vectorlayer.file_path = file_path
	vectorlayer.file_name = file_name
	vectorlayer.srs_wkt=src_spatial_ref.ExportToWkt()
	vectorlayer.geom_type=geometry_type
	vectorlayer.encoding=encoding
	vectorlayer.title=title
	vectorlayer.abstract=abstract
	vectorlayer.data_date=data_date
	vectorlayer.categories_string=categories_string
	vectorlayer.owner=owner
	vectorlayer.type="vector"
	vectorlayer.bbox = bbox

	vectorlayer.save()
	
	updateResult(errorMsg = None, percent_progress = 90)

	deleteTempFolder(temp_dir)

	return updateResult(errorMsg = None, percent_progress = 100)

'''
Diccionario con el resultado de la operacion.
Este  diccionario  estara dentro de un objeto 
celery.result.AsyncResult
result = {
			"error": string  con  mensaje de error, 
					 si no hay error, esta clave no 
					 sera None
			"percent": porcentaje de progreso de la
					   operacion
		}
'''
def updateResult(errorMsg, percent_progress):
	result = {}
	if(errorMsg):
		result["error"]=errorMsg
	if(percent_progress):
		result["percent"]=percent_progress
	current_task.update_state(state='PROGRESS',meta=result)
	return result


def createFileName(file_name):
	ts = time.time()
	timestamp_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
	file_name = file_name + timestamp_str + ".json"
	return file_name

def deleteTempFolder(fullName):
	try:
		shutil.rmtree(fullName, ignore_errors=True)
	except OSError as e:
		print ("Error: %s - %s." % (e.filename, e.strerror))

def calculateBBox(minXs, minYs, maxXs, maxYs):
	minX = sorted(minXs)[0]
	minY = sorted(minYs)[0]
	maxX = sorted(maxXs,reverse=True)[0]
	maxY = sorted(maxYs,reverse=True)[0]

	coords = ((minX,minY),(minX,maxY),
		(maxX,maxY),(maxX,minY),(minX,minY))
	bbox = Polygon(coords)
	return bbox

