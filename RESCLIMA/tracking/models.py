from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.gis.db import models as gismodels
import RESCLIMA.settings as settings
from django.utils import timezone
from sensor.models import Sensor
from RESCLIMA import settings
from tracking.helpers import file_directory_path, validate_file_extension_config
# Create your models here.

class TracksFile(models.Model):
	# Informacion general
	descripcion = models.TextField(max_length=500,null=True)
	file = models.FileField(upload_to='gpxfile/', validators=[validate_file_extension_config])
	date_init = models.DateField()
	date_last = models.DateField()
	sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, blank=True, null=True)
	def __unicode__(self):
		return "%s" % (self.file)
	def __str__(self):
		return "%s" % (self.file)

class TrackPoint(models.Model):
	id_p = models.AutoField(primary_key=True)
	sensor = models.ForeignKey(Sensor, null=True,on_delete=models.CASCADE)
	tspoint = models.DateTimeField(default=timezone.now)
	measured_points = JSONField(default = dict)
	
	def __unicode__(self):
		return "%s %s %s %s" % (self.sensor,self.ts,self.measured_points)
	def __str__(self):
		return "%s %s %s %s" % (self.sensor,self.ts,self.measured_points)

	class Meta:
		verbose_name = "Trackpoint"
		verbose_name_plural = "Trackpoints"