from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from sensor.views import *

urlpatterns = [
    url(r'^create/$', login_required(SensoresCreate.as_view(), login_url='noAccess'), name='sensor_create'),
    url(r'^$', login_required(list_sensors), name='sensor_list'),
    url(r'^update/(?P<pk>\d+)/$', login_required(SensoresUpdate.as_view(), login_url='noAccess'), name='sensor_update'),
    url(r'^delete/(?P<pk>\d+)/$', login_required(SensorDelete.as_view(), login_url='noAccess'), name='sensor_delete'),
]