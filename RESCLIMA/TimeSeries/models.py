from django.db import models

class Sensor(models.Model):
    #atributos
    serialNum = models.CharField(max_length=255)
    model = models.CharField(max_length=50, choices=(("BLOOMSKY", "Bloomsky - Sky2"),("NIPONCF", "NEI - CF200"),
                                                     ("HOBO", "Hobo")))
    #Falta definir tipo de dato de ubicacion
    location = models.CharField(max_length=50)

    #metodos
    def __unicode__(self):
        return "%s %s" % (self.numSerie,self.marca,self.ubicacion)
    def __str__(self):
        return "%s %s" % (self.numSerie,self.marca,self.ubicacion)

    class Meta:
        verbose_name = "Sensor"
        verbose_name_plural = "Sensors"

class Variable(models.Model):
    #atributos
    name = models.CharField(max_length=255)#Falta definir tipo de dato de ubicacion
    description = models.TextField()

    #metodos
    def __unicode__(self):
        return "%s %s" % (self.nombre,self.descripcion)
    def __str__(self):
        return "%s %s" % (self.nombre,self.descripcion)

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
        return "%s %s" % (self.date_time,self.valor)
    def __str__(self):
        return "%s %s" % (self.date_time, self.valor)

    class Meta:
        verbose_name = "Measurement"
        verbose_name_plural = "Measurements"


