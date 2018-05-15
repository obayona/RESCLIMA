from django.db import models
from django.contrib.gis.db import models

class Sensor(models.Model):
    #atributos
    serialNum = models.CharField(max_length=255)
    model = models.CharField(max_length=50)
    location = models.PointField(srid=4326, null=True)

    #metodos
    def __unicode__(self):
        return "%s %s" % (self.serialNum,self.model,self.location)
    def __str__(self):
        return "%s %s" % (self.serialNum,self.model,self.location)

    class Meta:
        verbose_name = "Sensor"
        verbose_name_plural = "Sensors"

class Variable(models.Model):
    #atributos
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    unit = models.CharField(max_length=100)

    #metodos
    def __unicode__(self):
        return "%s %s" % (self.name,self.description,self.unit)
    def __str__(self):
        return "%s %s" % (self.name,self.description,self.unit)

    class Meta:
        verbose_name = "Variable"
        verbose_name_plural = "Variables"

class SensorVariable(models.Model):
    #relaciones
    id_sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    id_variable = models.ForeignKey(Variable, on_delete=models.CASCADE)
    
    #metodos
    def __unicode__(self):
        return "%s %s" % (self.id_sensor,self.id_variable)
    def __str__(self):
        return "%s %s" % (self.id_sensor,self.id_variable)

    class Meta:
        verbose_name = "SensorVariable"
        verbose_name_plural = "SensorsVariables"

class Measurement(models.Model):
    #relaciones
    id_sensorVariable = models.ForeignKey(SensorVariable, on_delete=models.CASCADE)

    #atributos
    date_time = models.DateTimeField()
    value = models.FloatField()

    #metodos
    def __unicode__(self):
        return "%s %s" % (self.date_time,self.value)
    def __str__(self):
        return "%s %s" % (self.date_time, self.value)

    class Meta:
        verbose_name = "Measurement"
        verbose_name_plural = "Measurements"


