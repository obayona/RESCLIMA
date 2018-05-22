
from django.conf.urls import patterns, url

urlpatterns = patterns('RasterLayers.views',
	url(r'^$','list_rasterlayers'),
	url(r'^import$', 'import_geotiff'),
	url(r'^view$', 'view_geotiff'),
)