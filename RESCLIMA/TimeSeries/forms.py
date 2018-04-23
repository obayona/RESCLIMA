from django import forms
from .models import *

class SensorForm(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = [
            'serialNum',
            'brand',
            'model',
            'location',
        ]
        labels = {
            'serialNum': 'Numero de serie',
            'brand': 'Marca del sensor',
            'model': 'Modelo del sensor',
            'location': 'Ubicacion',
        }
        widgets = {
            'serialNum': forms.TextInput(attrs={'class': 'form-control', 'id': 'serialNum',
                                             'placeholder': 'Numero de serie aquí'}),

            'brand': forms.TextInput(attrs={'class': 'form-control', 'id': 'brand',
                                             'placeholder': 'Marca del sensor aquí'}),

            'model': forms.TextInput(attrs={'class': 'form-control', 'id': 'model',
                                               'placeholder': 'Modelo del sensor aquí'}),

            'location': forms.TextInput(attrs={'class': 'form-control', 'id': 'location',
                                                'placeholder': 'Ubicacion del sensor aquí'}),
        }

