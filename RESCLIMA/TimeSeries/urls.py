from django.conf.urls import patterns, url
from TimeSeries.views import *

urlpatterns = [
    url(r'^nuevoSensor/$', newSensor, name="newSensor"),
]