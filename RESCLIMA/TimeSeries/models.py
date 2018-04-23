from django.db import models

class Sensor(models.Model):
    #atributos
    numSerie = models.CharField(max_length=255)
    marca = models.CharField(max_length=255)
    modelo = models.CharField(max_length=255)
    #Falta definir tipo de dato de ubicacion
    ubicacion = models.CharField(max_length=50)

    #metodos
    def __unicode__(self):
        return "%s %s" % (self.numSerie,self.marca,self.ubicacion)
    def __str__(self):
        return "%s %s" % (self.numSerie,self.marca,self.ubicacion)

    class Meta:
        verbose_name = "Sensor"
        verbose_name_plural = "Sensores"

class Variable(models.Model):
    #atributos
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    sensores = models.ManyToManyField(Sensor)

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
        verbose_name_plural = "SensoresVariables"

class Medida(models.Model):
    #relaciones
    id_sensorVariable = models.ForeignKey(SensorVariable, on_delete=models.CASCADE)

    #atributos
    date_time = models.DateTimeField()
    valor = models.FloatField()

    #metodos
    def __unicode__(self):
        return "%s %s" % (self.date_time,self.valor)
    def __str__(self):
        return "%s %s" % (self.date_time, self.valor)

    class Meta:
        verbose_name = "Medida"
        verbose_name_plural = "Medidas"


