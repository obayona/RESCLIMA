from django.contrib.gis.db import models

class ShapeFile(models.Model):
	filename = models.CharField(max_length= 255)
	srs_wkt = models.CharField(max_length= 255)
	geom_type = models.CharField(max_length= 50)
	encoding = models.CharField(max_length= 20)

class Attribute(models.Model):
	shapefile = models.ForeignKey(ShapeFile)
	name = models.CharField(max_length= 255)
	type = models.IntegerField()
	width = models.IntegerField()
	precision = models.IntegerField()

class Feature(models.Model):
	shapefile =  models.ForeignKey(ShapeFile)
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