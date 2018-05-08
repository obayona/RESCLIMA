from django import forms
from django.contrib.gis import forms
#from mapwidgets.widgets import GooglePointFieldWidget
from TimeSeries.models import *
import floppyforms.__future__ as forms

CHARACTER_ENCODINGS = [("ascii",  "ASCII"),
                       ("latin1", "Latin-1"),
                       ("utf8",   "UTF-8")]

SENSOR_CHOICES = (
    ("BLOOMSKY", "Bloomsky - Sky2"),
    ("NIPONCF", "NEI - CF200"),
    ("HOBO", "Hobo"),
)

class SensorForm(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = [
            'serialNum',
            'model',
            'location',
        ]
        labels = {
            'serialNum': 'Numero de serie',
            'model': 'Modelo del sensor',
            'location': 'Ubicacion',
        }
        widgets = {
            'serialNum': forms.TextInput(attrs={'class': 'form-control', 'id': 'serialNum','placeholder': 'Numero de serie aqui'}),

            'model': forms.Select(attrs={'class':'form-control','id':'model','placeholder':'Seleccione modelo del sensor'}, choices=SENSOR_CHOICES),

            #'location': forms.gis.PointField(attrs={'class': 'form-control', 'id': 'location'}),
        }

class UploadFileForm(forms.Form):
    select = forms.CharField(widget=forms.Select(choices=SENSOR_CHOICES))
    file = forms.FileField()
    

