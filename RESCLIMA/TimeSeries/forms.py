from django import forms
from django.contrib.gis import forms
#from mapwidgets.widgets import GooglePointFieldWidget
from TimeSeries.models import *
#import floppyforms.__future__ as forms

CHARACTER_ENCODINGS = [("ascii",  "ASCII"),
                       ("latin1", "Latin-1"),
                       ("utf8",   "UTF-8")]

SENSOR_CHOICES = (
    ("BLOOMSKY", "Bloomsky - Sky2"),
    ("NIPONCF", "NEI - CF200"),
    ("HOBO", "Hobo"),
)
BRAND_CHOICES = (
    ("BLOOMSKY", "Bloomsky"),
    ("NIPONCF", "NIPONCF"),
    ("HOBO", "Hobo"),
)
MODEL_CHOICES = (
    ("SKY2", "Sky2"),
    ("NEI - CF200", "NEI - CF200"),
    ("HOBO", "Hobo"),
)


class StationTypeForm(forms.ModelForm):
    class Meta:
        model = StationType
        fields = [
            'brand',
            'model',
        ]
        labels = {
            'brand': 'Marca de la estacion',
            'model': 'Modelo de la estacion',
        }
        widgets = {
            'brand': forms.Select(attrs={'class':'form-control','id':'brand','placeholder':'Seleccione la marca de la estacion'}, choices=BRAND_CHOICES),
            'model': forms.Select(attrs={'class':'form-control','id':'model','placeholder':'Seleccione modelo de la estacion'}, choices=MODEL_CHOICES),

            #'location': forms.gis.PointField(attrs={'class': 'form-control', 'id': 'location'}),
        }

class StationForm(forms.Form):
    MODEL_CHOICES2 = []
    stations = StationType.objects.all()
    for station in stations:
        brand = station.brand
        model = station.model
        choice_name = brand+"-"+model
        pair = (choice_name,choice_name)
        MODEL_CHOICES2.append(pair)

    stationType = forms.CharField(label="Station Type", widget=forms.Select(choices=MODEL_CHOICES2))
    serialNum = forms.CharField(label="Serial Number",widget=forms.TextInput())
    latitude = forms.FloatField(label="Latitude",required=False, widget=forms.NumberInput(attrs={'step': '0.000001'}))
    longitude = forms.FloatField(label="Longitude", required=False, widget=forms.NumberInput(attrs={'step': '0.000001'}))
    frequency = forms.IntegerField(label="Requests frequency", required=False, widget=forms.NumberInput(attrs={'step': '1'}))
    token = forms.CharField(label="Access token", required=False, widget=forms.TextInput())

class UploadFileForm(forms.Form):
    MODEL_CHOICES2 = []
    stations = StationType.objects.all()
    for station in stations:
        brand = station.brand
        model = station.model
        choice_name = brand+"-"+model
        pair = (choice_name,choice_name)
        MODEL_CHOICES2.append(pair)

    select = forms.CharField(widget=forms.Select(choices=MODEL_CHOICES2))
    file = forms.FileField()
