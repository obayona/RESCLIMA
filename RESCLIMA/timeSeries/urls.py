from django.conf.urls import url
from timeSeries.views import *

urlpatterns = [
	url(r'^$',home, name="ts_home"),
	url(r'^import/station/$', import_station, name="ts_importstation"),
	url(r'^import/file/$', import_file, name="ts_importfile"),
	url(r'^view/$', visualize, name="ts_visualize"),
	url(r'^measurements/(?P<variable_id>\d+)/(?P<station_id>\d+)/(?P<startdate>\d{4}-\d{2}-\d{2})/(?P<enddate>\d{4}-\d{2}-\d{2})/$', get_measurements, name="ts_measurements"),
]
