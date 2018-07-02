# -*- coding: utf-8 -*-
from django.contrib.gis.db import models

class Style(models.Model):
	file_path = models.CharField(max_length=255)
	file_name = models.CharField(max_length=50)
	title = models.CharField(max_length=50)

	class Meta:
		ordering = ['id']

class RasterLayer(models.Model):
	file_path = models.CharField(max_length=255)
	file_name = models.CharField(max_length=50)
	file_format = models.CharField(max_length=10)
	projected = models.BooleanField(default=True)
	title = models.CharField(max_length=50,null=True)
	abstract = models.TextField(max_length=500,null=True)
	data_date = models.DateField(blank=True,null=True)
	upload_date = models.DateTimeField(auto_now_add=True)
	srs_wkt = models.TextField(max_length= 500)
	bbox = models.PolygonField(srid=4326,null=True)
	numBands = models.IntegerField(default=1)
	style = models.ForeignKey(Style, null=True)
