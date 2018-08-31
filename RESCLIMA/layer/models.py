from django.contrib.gis.db import models


# Create your models here.
class Layer(models.Model):
	title = models.CharField(max_length=50,null=True)
	abstract = models.TextField(max_length=500,null=True)
	type = models.CharField(max_length=10)
	data_date = models.DateField(blank=True,null=True)
	upload_date = models.DateTimeField(auto_now_add=True)
	srs_wkt = models.TextField(max_length= 500)
	bbox = models.PolygonField(srid=4326,null=True)
	#owner

class Category(models.Model):
    name = models.CharField(max_length=100)
    variables = models.ManyToManyField(Layer, blank = True)

    def __unicode__(self):
        return "%s-%s" % (self.name)
    def __str__(self):
        return "%s-%s" % (self.name)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

