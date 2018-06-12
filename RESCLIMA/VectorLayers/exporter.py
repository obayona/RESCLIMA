import os, os.path, tempfile, zipfile
import shutil, traceback
from osgeo import ogr
from models import VectorLayer, Attribute, Feature, AttributeValue
import utils
from django.contrib.gis.geos.geometry import GEOSGeometry
from osgeo import osr
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
import json


def export_data(vectorlayer):
	dst_dir = tempfile.mkdtemp()
	dst_file = str(os.path.join(dst_dir, vectorlayer.filename))
	dst_spatial_ref = osr.SpatialReference()
	dst_spatial_ref.ImportFromWkt(vectorlayer.srs_wkt)
	driver = ogr.GetDriverByName("ESRI shapefile")
	datasource = driver.CreateDataSource(dst_file)
	layer = datasource.CreateLayer(str(vectorlayer.filename),dst_spatial_ref)

	for attr in vectorlayer.attribute_set.all():
		field = ogr.FieldDefn(str(attr.name), attr.type)
		field.SetWidth(attr.width)
		field.SetPrecision(attr.precision)
		layer.CreateField(field)

	src_spatial_ref = osr.SpatialReference()
	src_spatial_ref.ImportFromEPSG(4326)
	coord_transform = osr.CoordinateTransformation(src_spatial_ref, dst_spatial_ref)
	geom_field = utils.calc_geometry_field(vectorlayer.geom_type)

	for feature in vectorlayer.feature_set.all():
		geometry = getattr(feature, geom_field)
		geometry = utils.unwrap_geos_geometry(geometry)
		dst_geometry = ogr.CreateGeometryFromWkt(geometry.wkt)
		dst_geometry.Transform(coord_transform)
		dst_feature = ogr.Feature(layer.GetLayerDefn())
		dst_feature.SetGeometry(dst_geometry)

		for attr_value in feature.attributevalue_set.all():
			utils.set_ogr_feature_attribute(
			attr_value.attribute,
			attr_value.value,
			dst_feature,
			vectorlayer.encoding)

		layer.CreateFeature(dst_feature)
		dst_feature.Destroy()

	datasource.Destroy()

	"""
	temp = tempfile.TemporaryFile()
	zip = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
	vectorlayer_base = os.path.splitext(dst_file)[0]
	vectorlayer_name = os.path.splitext(vectorlayer.filename)[0]
	
	for fName in os.listdir(dst_dir):
		print os.path.join(dst_dir, fName), fName
		zip.write(os.path.join(dst_dir, fName), fName)
	#zip.close()

	#shutil.rmtree(dst_dir)

	"""
	vectorlayer_name = os.path.splitext(vectorlayer.filename)[0]
	shutil.make_archive(os.path.join("/tmp",vectorlayer_name), 'zip', dst_dir);
	temp = open(os.path.join("/tmp",vectorlayer_name+".zip"),"r")
	f = FileWrapper(temp)
	response = HttpResponse(f, content_type="application/zip")
	response['Content-Disposition'] = "attachment; filename=" + vectorlayer_name + ".zip"
	response['Content-Length'] = temp.tell()
	temp.seek(0)
	shutil.rmtree(dst_dir)
	

	return response


def export_geojson(vectorlayer):
	geojson = {}
	geojson["type"] = "FeatureCollection";
	x = vectorlayer.centroid.x
	y = vectorlayer.centroid.y
	geojson["centroid"] = {"lon":x,"lat":y};
	geojson["crs"] = {"type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" }}
	geojson["features"] = []

		
	geom_field = utils.calc_geometry_field(vectorlayer.geom_type)
	for feature in vectorlayer.feature_set.all():
		geometry = getattr(feature, geom_field)
		geometry = utils.unwrap_geos_geometry(geometry)
		dst_geometry = ogr.CreateGeometryFromWkt(geometry.wkt)
		feature_json = {}
		feature_json["type"]="Feature";
		geometry_json = dst_geometry.ExportToJson();
		feature_json["geometry"] = json.loads(geometry_json);
		feature_json["properties"] = {};
		geojson["features"].append(feature_json);

		for attr_value in feature.attributevalue_set.all():
			value = attr_value.value;
			attr = attr_value.attribute;
			attr_name = attr_value.attribute.name;
			value = utils.getAttrValue(attr,value,vectorlayer.encoding)
			feature_json["properties"][attr_name] = value;
			
	return geojson