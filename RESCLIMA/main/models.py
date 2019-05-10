from django.db import models

from django.contrib.auth.models import User

class Researcher(models.Model):
	#relaciones
	usuario = models.OneToOneField(User, related_name="researcher", on_delete=models.CASCADE)
	
	#atributos
	identity_card = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=10)
	institution = models.CharField(max_length=100)

	#metodos
	def __unicode__(self):
		return "%s %s" % (self.name,self.institution)
	def __str__(self):
		return "%s %s" % (self.name, self.institution)

	class Meta:
		verbose_name = "Researcher"
		verbose_name_plural = "Researchers"
