# -*- coding: utf-8 -*-
from django import forms
from django.contrib.gis import forms
from TimeSeries.models import *

def getModelChoices(automatic):
    model_choices = []
    if(automatic==None):
        station_types = StationType.objects.all()
    else:    
        station_types = StationType.objects.filter(automatic=automatic)
    
    for station_type in station_types:
        choice_name = str(station_type)
        pair = (station_type.id,choice_name)
        model_choices.append(pair);
    
    return model_choices

class StationForm(forms.Form):
    model_choices = getModelChoices(automatic=None)
    stationType = forms.CharField(widget=forms.Select(choices=model_choices))
    serialNum = forms.CharField(label=u"Número serial",widget=forms.TextInput())
    latitude = forms.FloatField(label="Latitud",required=False, widget=forms.NumberInput(attrs={'step': '0.000001'}))
    longitude = forms.FloatField(label="Longitud", required=False, widget=forms.NumberInput(attrs={'step': '0.000001'}))
    frequency = forms.IntegerField(label="Frecuencia de requerimientos (en minutos)", required=False, widget=forms.NumberInput(attrs={'step': '1'}))
    token = forms.CharField(label="Token", required=False, widget=forms.TextInput())

class UploadFileForm(forms.Form):
    model_choices = getModelChoices(automatic=False)
    stationType = forms.CharField(widget=forms.Select(choices=model_choices))
    file = forms.FileField()
