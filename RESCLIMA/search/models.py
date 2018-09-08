from django.db import models
from django.contrib.postgres.search import SearchVector,SearchQuery, SearchRank, SearchVectorField

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s-%s" % (self.name)
    def __str__(self):
        return "%s-%s" % (self.name)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

class FilterSearchTable(models.Model):
    ts_vector = SearchVectorField(null = True)
    categories = models.ManyToManyField(Category, blank = True)
    class Meta:
        abstract = True