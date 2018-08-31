# -*- encoding: utf-8 -*-

from django import forms
from django.forms import extras

class ImportRasterForm(forms.Form):
    import_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}),label="Importar archivo raster")
    title = forms.CharField(label=u"Título")
    abstract = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "40", 'rows': "10", }),label=u"Resumen")

class ImportStyleForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(),label="Importar archivo SLD 1.1.0")
    title = forms.CharField(label=u"Título")