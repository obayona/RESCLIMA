from django.contrib.gis.db import models
from RESCLIMA import settings
from os.path import join

class VectorLayer(models.Model):

	filename = models.CharField(max_length= 255)
	srs_wkt = models.TextField(max_length= 500)
	geom_type = models.CharField(max_length= 50)
	encoding = models.CharField(max_length= 20)
	title = models.CharField(max_length=50,null=True)
	abstract = models.TextField(max_length=500,null=True)
	centroid = models.PointField(srid=4326,null=True)
	data_date = models.DateField(blank=True,null=True)
	upload_date = models.DateTimeField(auto_now_add=True)
	#bbox
	#owner

class Attribute(models.Model):
	vectorlayer = models.ForeignKey(VectorLayer)
	name = models.CharField(max_length= 255)
	type = models.IntegerField()
	width = models.IntegerField()
	precision = models.IntegerField()

class Feature(models.Model):
	vectorlayer = models.ForeignKey(VectorLayer)
	geom_point = models.PointField(srid=4326,blank=True,null=True)
	geom_multipoint = models.MultiPointField(srid=4326,blank=True,null=True)
	geom_multilinestring = models.MultiLineStringField(srid=4326,blank=True,null=True)
	geom_multipolygon = models.MultiPolygonField(srid=4326,blank=True,null=True)
	geom_geometrycollection = models.GeometryCollectionField(srid=4326,blank=True,null=True)

	objects = models.GeoManager()


class AttributeValue(models.Model):
	feature = models.ForeignKey(Feature)
	attribute = models.ForeignKey(Attribute)
	value = models.CharField(max_length=255,blank=True,null=True)

def getFileName(instance, filename):
	path = settings.STYLE_FILES_PATH;
	fullName = join(path,"style_{0}_{1}")
	return fullName.format(instance.vector.id, filename);
	
class Style(models.Model):
	file_path = models.FileField(upload_to=getFileName)
	title = models.CharField(max_length=50)
	vectorlayer = models.ForeignKey(VectorLayer)
