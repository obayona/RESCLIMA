from django.contrib.gis.db import models
from search.models import FilterSearchTable
from main.models import Researcher

# Create your models here.
class Layer(FilterSearchTable):
	title = models.CharField(max_length=50,null=True)
	abstract = models.TextField(max_length=1000,null=True)
	data_date = models.DateField(blank=True,null=True)
	upload_date = models.DateTimeField(auto_now_add=True)
	
	srs_wkt = models.TextField(max_length= 500)
	bbox = models.PolygonField(srid=4326,null=True)
	
	file_path = models.CharField(max_length=255)
	file_name = models.CharField(max_length=255)

	type = models.CharField(max_length=10)
	author = models.CharField(max_length=50, null=True)
	owner = models.ForeignKey(Researcher, null=True)

