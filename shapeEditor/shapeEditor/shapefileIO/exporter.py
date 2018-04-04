import os, os.path, tempfile, zipfile
import shutil, traceback
from osgeo import ogr
from shapeEditor.shared.models import ShapeFile, Attribute, Feature, AttributeValue
from shapeEditor.shared import utils
from django.contrib.gis.geos.geometry import GEOSGeometry
from osgeo import osr
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper


def export_data(shapefile):
	dst_dir = tempfile.mkdtemp()
	dst_file = str(os.path.join(dst_dir, shapefile.filename))
	dst_spatial_ref = osr.SpatialReference()
	dst_spatial_ref.ImportFromWkt(shapefile.srs_wkt)
	driver = ogr.GetDriverByName("ESRI Shapefile")
	datasource = driver.CreateDataSource(dst_file)
	layer = datasource.CreateLayer(str(shapefile.filename),dst_spatial_ref)

	for attr in shapefile.attribute_set.all():
		field = ogr.FieldDefn(str(attr.name), attr.type)
		field.SetWidth(attr.width)
		field.SetPrecision(attr.precision)
		layer.CreateField(field)

	src_spatial_ref = osr.SpatialReference()
	src_spatial_ref.ImportFromEPSG(4326)
	coord_transform = osr.CoordinateTransformation(src_spatial_ref, dst_spatial_ref)
	geom_field = utils.calc_geometry_field(shapefile.geom_type)

	for feature in shapefile.feature_set.all():
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
			shapefile.encoding)

		layer.CreateFeature(dst_feature)
		dst_feature.Destroy()

	datasource.Destroy()

	"""
	temp = tempfile.TemporaryFile()
	zip = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
	shapefile_base = os.path.splitext(dst_file)[0]
	shapefile_name = os.path.splitext(shapefile.filename)[0]
	
	for fName in os.listdir(dst_dir):
		print os.path.join(dst_dir, fName), fName
		zip.write(os.path.join(dst_dir, fName), fName)
	#zip.close()

	#shutil.rmtree(dst_dir)

	"""
	shapefile_name = os.path.splitext(shapefile.filename)[0]
	shutil.make_archive(join("/tmp",shapefile_name), 'zip', dst_dir);
	temp = open(join("/tmp",shapefile_name),"r")
	f = FileWrapper(temp)
	response = HttpResponse(f, content_type="application/zip")
	response['Content-Disposition'] = "attachment; filename=" + shapefile_name + ".zip"
	response['Content-Length'] = temp.tell()
	temp.seek(0)
	shutil.rmtree(dst_dir)
	

	return response
