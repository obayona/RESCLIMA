# -*- encoding: utf-8 -*-

import os, os.path, tempfile, zipfile
import shutil, traceback
from osgeo import ogr
from models import VectorLayer, Attribute, Feature, AttributeValue
from django.contrib.gis.geos import Point
from django.db import transaction
import utils
import datetime
from django.contrib.gis.geos.geometry import GEOSGeometry
from osgeo import osr


def get_data_date(request):
	year = int(request.POST["data_date_year"])
	month = int(request.POST["data_date_month"])
	day = int(request.POST["data_date_day"])
	return datetime.datetime(year=year,month=month,day=day)

@transaction.atomic
def import_data(request):
	# se obtienen las variables del POST
	list_files = request.FILES.getlist('import_files')
	encoding  = request.POST['encoding']
	title = request.POST["title"]
	abstract = request.POST["abstract"]
	data_date = get_data_date(request)

	# se verifica que esten todos los archivos requeridos
	required_suffixes = [".shp", ".shx", ".dbf", ".prj"]
	has_suffix = {}
	for suffix in required_suffixes:
		has_suffix[suffix] = False

	for file in list_files:
		extension = os.path.splitext(file.name)[1].lower()
		if extension in required_suffixes:
			has_suffix[extension] = True

	for suffix in required_suffixes:
		if not has_suffix[suffix]:
			return "Archivo perdido requerido ."+suffix

	# se guardan los archivos en una carpeta temporal
	dst_dir = tempfile.mkdtemp()
	vectorlayer_name = None # nombre del archivo shapefile
	
	for file in list_files:
		# si la extencion  del archivo es shp
		# este sera el nombre del archivo
		if file.name.endswith(".shp"):
			vectorlayer_name = file.name

		# se guarda el archivo en la carpeta temporal
		file_dir = os.path.join(dst_dir,file.name)
		f = open(file_dir, 'wb+')	
		for chunk in file.chunks():
			f.write(chunk)
		f.close()

	# se abre el shapefile con la libreria OGR
	try:
		datasource = ogr.Open(os.path.join(dst_dir,vectorlayer_name))
		layer = datasource.GetLayer(0)
		vectorlayerOK = True
	except:
		traceback.print_exc()
		vectorlayerOK = False
	if not vectorlayerOK:
		# si la capa no es valida se borra la carpeta temporal
		shutil.rmtree(dst_dir)
		return "La capa vectorial no es válida"

	src_spatial_ref = layer.GetSpatialRef() # se obtiene la referencia espacial src
	geometry_type = layer.GetLayerDefn().GetGeomType() # se obtiene el tipo de geometria del shapefile
	geometry_name = utils.ogr_type_to_geometry_name(geometry_type)

	# se crea el objeto vectorlayer del modelo
	vectorlayer_name = os.path.splitext(file.name)[0].lower()
	vectorlayer = VectorLayer(filename=vectorlayer_name,
							  srs_wkt=src_spatial_ref.ExportToWkt(),
							  geom_type=geometry_name,
							  encoding=encoding,
							  title=title,
							  abstract=abstract,
							  data_date=data_date)
	vectorlayer.save()
	# se obtienen los atributos del shapefile
	# y se crean objetos Attribute del modelo
	attributes = []
	layer_def = layer.GetLayerDefn()
	field_count = range(layer_def.GetFieldCount())
	for i in field_count:
		field_def = layer_def.GetFieldDefn(i)
		attr = Attribute(vectorlayer=vectorlayer,
	                     name=field_def.GetName(),
	                     type=field_def.GetType(),
	                     width=field_def.GetWidth(),
	                     precision=field_def.GetPrecision())
		attr.save()
		attributes.append(attr)

	# se crea la referencia EPSG:4326
	dst_spatial_ref = osr.SpatialReference()
	dst_spatial_ref.ImportFromEPSG(4326)
	coord_transform = osr.CoordinateTransformation(src_spatial_ref,dst_spatial_ref)

	# se extraen y se guardan los features del shapefile
	pointsX = []
	pointsY = []
	feature_count = range(layer.GetFeatureCount())
	for i in feature_count:
		src_feature = layer.GetFeature(i)
		src_geometry = src_feature.GetGeometryRef()
		src_geometry.Transform(coord_transform)
		geometry = GEOSGeometry(src_geometry.ExportToWkt())
		geometry = utils.wrap_geos_geometry(geometry)
		# se guarda el centroide de cada geometria
		centroid = geometry.centroid
		pointsX.append(centroid.x)
		pointsY.append(centroid.y)
		
		geometry_field = utils.calc_geometry_field(geometry_name)
		args = {}
		args['vectorlayer'] = vectorlayer
		args[geometry_field] = geometry
		feature = Feature(**args)
		feature.save()
		# se guardan los valores de los atributos
		for attr in attributes:
			success,result = utils.getOGRFeatureAttribute(attr, src_feature,encoding)
			if not success:
				shutil.rmtree(dst_dir)
				vectorlayer.delete()
				return result
			attr_value = AttributeValue(feature=feature,attribute=attr,value=result)
			attr_value.save()


	# se calcula el centroide
	x = sum(pointsX)/float(len(pointsX))
	y = sum(pointsY)/float(len(pointsY))
	centroid = Point(x,y)
	vectorlayer.centroid = centroid
	vectorlayer.save()
	shutil.rmtree(dst_dir)

	return None