# -*- encoding: utf-8 -*-

from django import forms
from django.forms import extras

class ImportGeotiffForm(forms.Form):
    import_files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),label="Importar geotiff")
    title = forms.CharField(label=u"Título")
    abstract = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "40", 'rows': "10", }),label=u"Resumen")