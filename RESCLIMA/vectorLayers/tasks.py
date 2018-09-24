# -*- encoding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
import shutil
import os
import datetime
from celery import shared_task, current_task
from django.db import transaction
from osgeo import ogr
from .models import VectorLayer, Attribute, Feature, AttributeValue
from osgeo import osr
from django.contrib.gis.geos.geometry import GEOSGeometry
from django.contrib.gis.geos import Polygon
import vectorLayers.utils as utils


@shared_task
@transaction.atomic
def import_vector_layer(vectorlayer_params):
	# se extraen los parametros del vector layer
	temp_dir = vectorlayer_params["temp_dir"]
	vectorlayer_name = vectorlayer_params["vectorlayer_name"]
	encoding  = vectorlayer_params["encoding"]
	title = vectorlayer_params["title"]
	abstract = vectorlayer_params["abstract"]
	date_str = vectorlayer_params["date_str"] # fecha como string
	data_date = datetime.datetime.strptime(date_str, '%Y-%m-%d') # fecha como objeto datetime
	categories_string = vectorlayer_params["categories_string"] # string de categorias


	result = {}
	# se abre el shapefile con la libreria OGR
	try:
		datasource = ogr.Open(os.path.join(temp_dir,vectorlayer_name))
		layer = datasource.GetLayer(0)
	except Exception as e:
		# pendiente se debe mandar al log
		x = os.path.join(temp_dir,vectorlayer_name)
		y = os.path.exists(x)
		print str(e)
		# si la capa no es valida se borra la carpeta temporal
		#shutil.rmtree(temp_dir)
		result["error"] = str(x) + str(y) +  " La capa vectorial no es válid " + str(e) + os.path.join(temp_dir,vectorlayer_name)
		#return {'current': total_user, 'total': total_user, 'percent': 100}
		return result

	# actualiza el porcentaje de avance de la tarea: 5%
	result["error"]=None
	result["percent"]=5
	current_task.update_state(state='PROGRESS',meta=result)


	src_spatial_ref = layer.GetSpatialRef() # se obtiene la referencia espacial de la capa
	geometry_type = layer.GetLayerDefn().GetGeomType() # se obtiene el tipo de geometria del shapefile
	geometry_name = utils.ogr_type_to_geometry_name(geometry_type)


	# se crea el objeto vectorlayer del modelo
	vectorlayer_name = os.path.splitext(vectorlayer_name)[0].lower()
	vectorlayer = VectorLayer(filename=vectorlayer_name,
							  srs_wkt=src_spatial_ref.ExportToWkt(),
							  geom_type=geometry_name,
							  encoding=encoding,
							  title=title,
							  abstract=abstract,
							  data_date=data_date,
							  categories_string=categories_string,
							  type="vector")
	vectorlayer.save()

	# actualiza el porcentaje de avance de la tarea: 10%
	result["error"]=None
	result["percent"]=10
	current_task.update_state(state='PROGRESS',meta=result)

	# se obtienen los atributos del shapefile
	# y se crean objetos Attribute del modelo
	attributes = []
	layer_def = layer.GetLayerDefn()
	num_fields = layer_def.GetFieldCount()
	field_count = range(num_fields)
	num_fields = float(num_fields)	

	for i in field_count:
		field_def = layer_def.GetFieldDefn(i)
		attr = Attribute(vectorlayer=vectorlayer,
	                     name=field_def.GetName(),
	                     type=field_def.GetType(),
	                     width=field_def.GetWidth(),
	                     precision=field_def.GetPrecision())
		attr.save()
		attributes.append(attr)
		# se actualiza el pocentaje de progreso
		# de 10% a 30%
		percent = 10.0 + (float(i)/num_fields)*20.0
		result["percent"]= percent
		current_task.update_state(state='PROGRESS',meta=result)

	# se crea la referencia EPSG:4326
	dst_spatial_ref = osr.SpatialReference()
	dst_spatial_ref.ImportFromEPSG(4326)
	# se crea un objeto para transformar los sistemas de coordenadas
	# de la capa original a 4326
	coord_transform = osr.CoordinateTransformation(src_spatial_ref,dst_spatial_ref)

	# se actualiza el progreso
	result["percent"]= 45
	current_task.update_state(state='PROGRESS',meta=result)
	# se extraen y se guardan los features del shapefile
	num_features = layer.GetFeatureCount()
	feature_count = range(num_features)
	num_features = float(num_features)
	minXs = []
	minYs = []
	maxXs = []
	maxYs = []

	for i in feature_count:
		src_feature = layer.GetFeature(i)
		src_geometry = src_feature.GetGeometryRef()
		src_geometry.Transform(coord_transform)
		# se extrae el envelope
		env = src_geometry.GetEnvelope()
		minXs.append(env[0])
		minYs.append(env[2])
		maxXs.append(env[1])
		maxYs.append(env[3])
		geometry = GEOSGeometry(src_geometry.ExportToWkt())
		geometry = utils.wrap_geos_geometry(geometry)
		
		geometry_field = utils.calc_geometry_field(geometry_name)
		args = {}
		args['vectorlayer'] = vectorlayer
		args[geometry_field] = geometry
		feature = Feature(**args)
		feature.save()
		# se guardan los valores de los atributos
		for attr in attributes:
			success,value = utils.getOGRFeatureAttribute(attr, src_feature,encoding)
			if not success:
				shutil.rmtree(temp_dir)
				vectorlayer.delete()
				# retorna un objeto con error
				result["error"]="Error al obtener los valores del atributo " + str(attr.name)
				return result
			attr_value = AttributeValue(feature=feature,attribute=attr,value=value)
			attr_value.save()
		# se actualiza el porcentaje de avance
		# de 45% a 80%
		percent = 45 + (float(i)/num_features)*35.0
		result["percent"]= percent
		current_task.update_state(state='PROGRESS',meta=result)

	# se obtiene el bounding box de la capa
	minX = sorted(minXs)[0]
	minY = sorted(minYs)[0]
	maxX = sorted(maxXs,reverse=True)[0]
	maxY = sorted(maxYs,reverse=True)[0]
	# se actualiza el progreso
	result["percent"]= 85
	current_task.update_state(state='PROGRESS',meta=result)

	coords = ((minX,minY),(minX,maxY),
		(maxX,maxY),(maxX,minY),(minX,minY))
	bbox = Polygon(coords)

	vectorlayer.bbox = bbox

	# se guarda la capa
	vectorlayer.save()
	# se actualiza el progreso
	result["percent"]= 90
	current_task.update_state(state='PROGRESS',meta=result)
	# se elimina la carpeta temporal
	shutil.rmtree(temp_dir)

	result["percent"]=100
	return result


