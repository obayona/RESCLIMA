from django.db import models
from Layer.models import Layer


class Style(models.Model):
	file_path = models.CharField(max_length=255)
	file_name = models.CharField(max_length=50)
	title = models.CharField(max_length=50)
	type = models.CharField(max_length=10)
	layers = models.ManyToManyField(Layer)
	#owner