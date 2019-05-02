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


'''class TrackFileForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=False)
    class Meta:
        model = TracksFile
        fields = ["descripcion"]
    date_init = forms.DateField(
        widget=forms.DateInput(format=('%YY-%mm-%d'), 
                               attrs={'class':'datepicker', 
                               'placeholder':'Select a date'}))
    date_last = forms.DateField(
        widget=forms.DateInput(format=('%YY-%mm-%d'), 
                               attrs={'class':'datepicker', 
                               'placeholder':'Select a date'}))
'''

class TrackFileForm(forms.ModelForm):

    #sensor = forms.ChoiceField(label='Sensor', widget=forms.Select, choices=sensor())
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':False}),required=True)
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user','')
        super(TrackFileForm, self).__init__(*args, **kwargs)
        self.fields['sensor']=forms.ModelChoiceField(queryset=Sensor.objects.all())

    class Meta:
        model = TracksFile
        fields = ["descripcion", 'date_init', 'date_last','file']
        widgets = {
            'date_init': DateInput(),
            'date_last': DateInput()
        }
