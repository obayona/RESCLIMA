from django.db import models
from django.contrib.postgres.search import SearchVector,SearchQuery, SearchRank, SearchVectorField

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s" % (self.name)
    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

class FilterSearchTable(models.Model):
    ts_index = SearchVectorField(null = True, blank=True)
    categories_string = models.TextField(null= True, blank = True, max_length= 600)
    class Meta:
        abstract = True