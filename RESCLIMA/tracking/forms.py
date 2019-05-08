from django import forms
from . models import *
from django.forms import widgets
from sensor.models import Sensor


class DateInput(forms.DateInput):
    input_type = 'date'

def sensor():
    sensorlist = []
    sensor = Sensor.objects.all()
    for sense in sensor:
        option = (sense.id, sense.name)
        sensorlist.append(option)
    return sensorlist

class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.name

class TrackFileForm(forms.ModelForm):

    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':False}),required=True)
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user','')
        super(TrackFileForm, self).__init__(*args, **kwargs)
        self.fields['sensor']=CustomModelChoiceField(queryset=Sensor.objects.all())

    class Meta:
        model = TracksFile
        fields = ["descripcion", 'date_init', 'date_last','file']
        widgets = {
            'date_init': DateInput(),
            'date_last': DateInput()
        }
