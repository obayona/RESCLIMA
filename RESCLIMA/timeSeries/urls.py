from django.conf.urls import url
from timeSeries.views import *

urlpatterns = [
    url(r'^$',show_options, name="show_options"),
    url(r'^import/$', upload_file, name="upload_file"),
    #url(r'^import_station/$', import_station, name="import_station"),
    url(r'^view/$', visualize, name="visualize"),
    url(r'^measurements/$', get_measurements, name="get_measurements"),


]

