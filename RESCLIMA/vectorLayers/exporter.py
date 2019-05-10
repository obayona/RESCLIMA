# -*- encoding: utf-8 -*-
import os, os.path, tempfile, zipfile
from os.path import join
import shutil, traceback
from osgeo import ogr
from vectorLayers.models import VectorLayer
from django.contrib.gis.geos.geometry import GEOSGeometry
from osgeo import osr
from django.http import HttpResponse
from wsgiref.util import FileWrapper
import simplejson as json
"""
Obtiene los  datos de una capa 
vectorial, crea un shapefile y 
retorna un HttpResponse con el 
archivo
"""
def export_shapefile(vectorlayer):

	file_path = vectorlayer.file_path
	file_name = vectorlayer.file_name
	full_path = join(file_path,file_name)

	encoding = vectorlayer.encoding
	srs_wkt = vectorlayer.srs_wkt
	geom_type = vectorlayer.geom_type

	f = open(full_path,"r", encoding=encoding)
	geojson = json.loads(f.read())
	f.close()

	dst_dir = tempfile.mkdtemp()
	shapefile_name = file_name.replace(".json",".shp")
	dst_file = join(dst_dir, shapefile_name)
	
	#sistema de coordenadas 4326
	src_spatial_ref = osr.SpatialReference()
	src_spatial_ref.ImportFromEPSG(4326)
	#sistema de coordenadas de la capa original
	dst_spatial_ref = osr.SpatialReference()
	dst_spatial_ref.ImportFromWkt(srs_wkt)
	coord_transform = osr.CoordinateTransformation(src_spatial_ref, dst_spatial_ref)

	driver = ogr.GetDriverByName("ESRI shapefile")
	datasource = driver.CreateDataSource(dst_file)	
	layer = datasource.CreateLayer(name = shapefile_name,
									srs = dst_spatial_ref,
									geom_type = geom_type)


	for i, attr in enumerate(geojson["attributes"]):	
		field = ogr.FieldDefn(attr["name"],attr["type"])
		field.SetWidth(attr["width"])
		field.SetPrecision(attr["precision"])
		layer.CreateField(field)

	for i, feature in enumerate(geojson["features"]):
		geometry = feature.get("geometry",None)
		if(geometry==None):
			continue
		dst_geometry = ogr.CreateGeometryFromJson(json.dumps(geometry))
		dst_feature = ogr.Feature(layer.GetLayerDefn())
		dst_feature.SetGeometry(dst_geometry)
		dst_geometry.Transform(coord_transform)

		properties = feature.get("properties",None)
		if properties==None:
			continue

		for field,value in properties.items():
			field = field.replace("\"","")
			field = field.replace("'","")
			dst_feature.SetField(field,value)

		layer.CreateFeature(dst_feature)
		dst_feature.Destroy()

	datasource.Destroy()

	zip_dst = file_name.replace(".json","_zip");
	zip_dst = shutil.make_archive(zip_dst, 'zip', dst_dir)
	shutil.rmtree(dst_dir)
	zip_file = open(zip_dst,"rb")

	f = FileWrapper(zip_file)
	response = HttpResponse(f, content_type="application/zip")
	zip_name = file_name.replace(".json",".zip")
	response['Content-Disposition'] = "attachment; filename=" + zip_name
	
	return response


"""
Obtiene los  datos d e una capa 
vectorial,  crea un diccionario
que   contiene un  geojson y lo
retorna 
"""
def export_geojson(vectorlayer):
	file_path = vectorlayer.file_path
	file_name = vectorlayer.file_name
	full_path = join(file_path,file_name)
	encoding = vectorlayer.encoding

	f = open(full_path,"r", encoding=encoding)
	geojson = f.read()
	f.close()
	return geojson
