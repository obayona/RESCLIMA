from django.contrib.gis.db import models
from RESCLIMA import settings
from os.path import join
from django.contrib.auth.models import User
from layer.models import Layer


class VectorLayer(Layer):
	geom_type = models.IntegerField()
	encoding = models.CharField(max_length= 20)
