from django.db import models
# from django.contrib.postgres.search import SearchVector,SearchQuery, SearchRank
from layer.models import Layer

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s-%s" % (self.name)
    def __str__(self):
        return "%s-%s" % (self.name)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

class SearchTable(models.Model):
    categories = models.ManyToManyField(Category, blank = True)
    def __unicode__(self):
        return "%s-%s" % (self.name)
    def __str__(self):
        return "%s-%s" % (self.name)

    class Meta:
        verbose_name = "TablaDeBusqueda"
        verbose_name_plural = "TablasDeBusqueda"
