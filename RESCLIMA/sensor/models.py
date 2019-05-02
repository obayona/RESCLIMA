from django.db import models

# Create your models here.
class Sensor(models.Model):
	name = models.CharField(max_length=20)
	date = models.DateField(auto_now=False, auto_now_add=False)
	description = models.TextField(max_length=500,null=True)

"""	class Meta:
		verbose_name= "Sensor"
		verbose_name_plural = "Sensores"""