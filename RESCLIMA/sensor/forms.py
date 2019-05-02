from django import forms
from sensor.models import *
from django.forms import SelectDateWidget
from django.forms import DateField

class SensorForm(forms.ModelForm):

    class Meta:
        model = Sensor
        fields = ['name','date','description']
        widgets = {
            'date': forms.DateInput(format=('%d-%m-%Y'), 
                                             attrs={'class':'myDateClass', 
                                            'placeholder':'Select a date'})
        }


