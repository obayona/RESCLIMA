from django import forms
from .models import *

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
            'serialNum': forms.TextInput(attrs={'class': 'form-control', 'id': 'serialNum',
                                             'placeholder': 'Numero de serie aquí'}),

            'model': forms.Select(attrs={'class':'form-control','id':'model',
                                            'placeholder':'Seleccione modelo del sensor'}),

            'location': forms.TextInput(attrs={'class': 'form-control', 'id': 'location',
                                                'placeholder': 'Ubicacion del sensor aquí'}),
        }

