from django.conf.urls import patterns, url

urlpatterns = patterns('TimeSeries.views',
    url(r'^nuevoSensor/$', newSensor, name="newSensor"),
)