from django.conf.urls import patterns, url
from TimeSeries.views import *

urlpatterns = [
    url(r'^$',show_options, name="show_options"),
    url(r'^import/$', upload_file, name="upload_file"),
    url(r'^newSensor/$', new_sensor, name="new_sensor"),
]