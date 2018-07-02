
from django.conf.urls import patterns, url

urlpatterns = patterns('tms.views',
	url(r'^$','root'), #ej "/tms" calls root()
  url(r'^(?P<version>[0-9.]+)$','service'), # ej, "/tms/1.0" calls service(version="1.0")
  url(r'^(?P<version>[0-9.]+)/' + r'(?P<rasterlayer_id>\d+)$','tileMap'), # eg, "/tms/1.0/2" calls tileMap(version="1.0", shapefile_id=2)
  url(r'^(?P<version>[0-9.]+)/' + r'(?P<rasterlayer_id>\d+)/(?P<zoom>\d+)/' + r'(?P<x>\d+)/(?P<y>\d+)\.png$','tile'), # eg, "/tms/1.0/2/3/4/5" calls tile(version="1.0", shapefile_id=2, zoom=3, x=4, y=5
)