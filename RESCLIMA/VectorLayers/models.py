from django.contrib.gis.db import models
from RESCLIMA import settings
from os.path import join
from django.contrib.auth.models import User



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


class Style(models.Model):
	file_path = models.CharField(max_length=255)
	file_name = models.CharField(max_length=50)
	title = models.CharField(max_length=50)
	vectorlayer = models.ForeignKey(VectorLayer)

	class Meta:
		ordering = ['id']


<<<<<<< HEAD
=======
class Researcher(models.Model):
	#relaciones
	usuario = models.OneToOneField(User, related_name="researcher", on_delete=models.CASCADE)
	
	#atributos
	identity_card = models.CharField(max_length=50)
	nombre = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=10)
	institution = models.CharField(max_length=100)

	#metodos
	def __unicode__(self):
		return "%s %s" % (self.nombre,self.institution)
	def __str__(self):
		return "%s %s" % (self.nombre, self.institution)

	class Meta:
		verbose_name = "Researcher"
		verbose_name_plural = "Researchers"

>>>>>>> remotes/origin/upload-files
