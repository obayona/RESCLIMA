from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.gis.db import models as gismodels
import RESCLIMA.settings as settings
from sensor.models import Sensor
from tracking.helpers import file_directory_path, validate_file_extension_config
# Create your models here.

class TracksFile(models.Model):
	# Informacion general
	descripcion = models.TextField(max_length=500,null=True)
	file = models.FileField(upload_to=file_directory_path, validators=[validate_file_extension_config])
	date_init = models.DateField()
	date_last = models.DateField()
	sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, blank=True, null=True)
	def __unicode__(self):
		return "%s" % (self.file)
	def __str__(self):
		return "%s" % (self.file)

class TrackPoint(models.Model):

	name = models.CharField(verbose_name="Nombre", max_length=100)
	sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
	date_start = models.DateField()
	date_end = models.DateField()
	measured_points = JSONField()
	#trackfile = models.ForeignKey(TracksFile, on_delete=models.CASCADE, blank=True, null=True)
