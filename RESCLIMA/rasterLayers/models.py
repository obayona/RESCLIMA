# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from layer.models import Layer

class RasterLayer(Layer):
	noValue = models.FloatField()
	numBands = models.IntegerField(default=1)
	
