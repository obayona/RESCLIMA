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


# Modelos para los datos de Logistica y Transporte
class Logistica(models.Model):
	VEHICLE_TYPE_CHOICES = (
	  (None, 'Seleccione una opción'),
	  (1, 'Liviano'),
	  (0, 'Pesado'),
	)
	MOVEMENT_TYPE_CHOICES = (
	  (None, 'Seleccione una opción'),
	  (1, 'GD Sentido E-N'),
	  (2, 'FR Sentido E-O'),
	  (3, 'GD Sentido N-O'),
	  (4, 'GI Sentido O-N'),
	  (5, 'FR Sentido O-E'),
	  (6, 'GI Sentido N-E'),
	)
	# Informacion general
	id_term = models.IntegerField()
	value = models.IntegerField()
	vehicle_type = models.PositiveSmallIntegerField(null=True, choices=VEHICLE_TYPE_CHOICES)
	movement = models.PositiveSmallIntegerField(null=True, choices=MOVEMENT_TYPE_CHOICES)
	id_gauging = models.IntegerField()
	date = models.DateField()
	# Foreign Key
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def get_vehicle_type(self):
		choices = {
	        1: "Liviano",
	        0: "Pesado"
	    }
		return choices.get(self.vehicle_type, "¡Choices error!")

	def get_movement(self):
		choices = {
	        1: "GD Sentido E-N",
	        2: "FR Sentido E-O",
	        3: "GD Sentido N-O",
	        4: "GI Sentido O-N",
	        5: "FR Sentido O-E",
	        6: "GI Sentido N-E"
	    }
		return choices.get(self.movement, "¡Choices error!")

	class Meta:
		verbose_name = "Logistica"
		verbose_name_plural = "Datos de Logistica"

# Modelos para los datos de cambio climatico e islas de calor
class Clima(models.Model):
	# Informacion general
	date = models.DateField()
	tmin = models.DecimalField(decimal_places=2, max_digits=10)
	tmax = models.DecimalField(decimal_places=2, max_digits=10)
	tmean = models.DecimalField(decimal_places=2, max_digits=10)
	rr = models.DecimalField(decimal_places=2, max_digits=10)
	oni = models.DecimalField(decimal_places=2, max_digits=10)
	# Foreign Key
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		verbose_name = "Clima"
		verbose_name_plural = "Datos de Clima"

class Censo(models.Model):
	# Informacion general
	year = models.CharField(max_length=4)
	man = models.IntegerField()
	woman = models.IntegerField()
	total_pob = models.IntegerField()
	lettered = models.IntegerField()
	unlettered = models.IntegerField()
	housing = models.IntegerField()
	# Foreign Key
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		verbose_name = "Censo"
		verbose_name_plural = "Datos de Censo"

# Modelos para los datos de Logistica y Transporte
class Logistica(models.Model):
	VEHICLE_TYPE_CHOICES = (
	  (None, 'Seleccione una opción'),
	  (1, 'Liviano'),
	  (0, 'Pesado'),
	)
	MOVEMENT_TYPE_CHOICES = (
	  (None, 'Seleccione una opción'),
	  (1, 'GD Sentido E-N'),
	  (2, 'FR Sentido E-O'),
	  (3, 'GD Sentido N-O'),
	  (4, 'GI Sentido O-N'),
	  (5, 'FR Sentido O-E'),
	  (6, 'GI Sentido N-E'),
	)
	# Informacion general
	id_term = models.IntegerField()
	value = models.IntegerField()
	vehicle_type = models.PositiveSmallIntegerField(null=True, choices=VEHICLE_TYPE_CHOICES)
	movement = models.PositiveSmallIntegerField(null=True, choices=MOVEMENT_TYPE_CHOICES)
	id_gauging = models.IntegerField()
	date = models.DateField()
	# Foreign Key
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def get_vehicle_type(self):
		choices = {
	        1: "Liviano",
	        0: "Pesado"
	    }
		return choices.get(self.vehicle_type, "¡Choices error!")

	def get_movement(self):
		choices = {
	        1: "GD Sentido E-N",
	        2: "FR Sentido E-O",
	        3: "GD Sentido N-O",
	        4: "GI Sentido O-N",
	        5: "FR Sentido O-E",
	        6: "GI Sentido N-E"
	    }
		return choices.get(self.movement, "¡Choices error!")

	class Meta:
		verbose_name = "Logistica"
		verbose_name_plural = "Datos de Logistica"

# Modelos para los datos de cambio climatico e islas de calor
class Clima(models.Model):
	# Informacion general
	date = models.DateField()
	tmin = models.DecimalField(decimal_places=2, max_digits=10)
	tmax = models.DecimalField(decimal_places=2, max_digits=10)
	tmean = models.DecimalField(decimal_places=2, max_digits=10)
	rr = models.DecimalField(decimal_places=2, max_digits=10)
	oni = models.DecimalField(decimal_places=2, max_digits=10)
	# Foreign Key
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		verbose_name = "Clima"
		verbose_name_plural = "Datos de Clima"

class Censo(models.Model):
	# Informacion general
	year = models.CharField(max_length=4)
	man = models.IntegerField()
	woman = models.IntegerField()
	total_pob = models.IntegerField()
	lettered = models.IntegerField()
	unlettered = models.IntegerField()
	housing = models.IntegerField()
	# Foreign Key
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		verbose_name = "Censo"
		verbose_name_plural = "Datos de Censo"
