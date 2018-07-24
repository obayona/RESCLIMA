from django.db import models
from Layer.models import Layer

class Category(models.Model):
    name = models.CharField(max_length=100)
    variables = models.ManyToManyField(Layer, blank = True)

    def __unicode__(self):
        return "%s-%s" % (self.name)
    def __str__(self):
        return "%s-%s" % (self.name)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
