# -*- encoding: utf-8 -*-

from django import forms
from django.forms import extras

CHARACTER_ENCODINGS = [("ascii",  "ASCII"),("latin1", "Latin-1"),("utf8",   "UTF-8")]

class ImportShapefileForm(forms.Form):
    import_files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),label="Importar archivos shapefile")
    encoding = forms.ChoiceField(choices=CHARACTER_ENCODINGS,label=u"Codificación") 
    title = forms.CharField(label=u"Título")
    abstract = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "40", 'rows': "10", }),label=u"Resumen")
    