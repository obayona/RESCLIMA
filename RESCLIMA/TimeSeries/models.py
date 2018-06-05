from django.db import models
from django.contrib.gis.db import models

class Variable(models.Model):
    #atributos
    name = models.CharField(max_length=50)
    unit = models.CharField(max_length=20)
    symbol = models.CharField(max_length=10)

    #metodos
    def __unicode__(self):
        return "%s %s" % (self.name,self.unit,self.symbol)
    def __str__(self):
        return "%s %s" % (self.name,self.unit,self.symbol)

    class Meta:
        verbose_name = "Variable"
        verbose_name_plural = "Variables"

class StationType(models.Model):
    #atributos
    brand = models.CharField(max_length=30)
    model = models.CharField(max_length=30)

    #metodos
    def __unicode__(self):
        return "%s %s" % (self.brand,self.model)
    def __str__(self):
        return "%s %s" % (self.brand,self.model)

    class Meta:
        verbose_name = "StationType"
        verbose_name_plural = "StationTypes"

class Station(models.Model):
    #atributos
    serialNum = models.CharField(max_length=30)
    location = models.PointField(srid=4326)
    active = models.BooleanField()
    stationType = models.ForeignKey(StationType, on_delete=models.CASCADE)

    #metodos
    def __unicode__(self):
        return "%s %s" % (self.serialNum,self.location,self.active,self.stationType)
    def __str__(self):
        return "%s %s" % (self.serialNum,self.location,self.active,self.stationType)

    class Meta:
        verbose_name = "Station"
        verbose_name_plural = "Station"


class Provider(models.Model):
    #relaciones
#    info = JSONField()

    #metodos
#    def __unicode__(self):
 #       return "%s %s" % (self.info)
  #  def __str__(self):
   #     return "%s %s" % (self.info)

    class Meta:
        verbose_name = "Provider"
        verbose_name_plural = "Provider"


class Measurement(models.Model):
    #relaciones
    idStation = models.ForeignKey(Station, null=True, on_delete=models.CASCADE)
    idProvider = models.ForeignKey(Provider, null=True, on_delete=models.CASCADE)

    #atributos
    datetime = models.DateTimeField(auto_now_add=True)
    #readings = JSONField()

    #value = models.FloatField()

    #metodos
#    def __unicode__(self):
 #       return "%s %s" % (self.idStation,self.idProvider,self.datetime,self.readings)
  #  def __str__(self):
   #     return "%s %s" % (self.idStation,self.idProvider,self.datetime,self.readings)

    class Meta:
        verbose_name = "Measurement"
        verbose_name_plural = "Measurements"

