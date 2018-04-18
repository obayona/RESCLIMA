from django.conf.urls import patterns, url

urlpatterns = patterns('VectorLayers.views',
	url(r'^$','list_vectorfiles'),
	url(r'^import$', 'import_shapefile'),
	url(r'^export/(?P<shapefile_id>\d+)$', 'export_shapefile'),
)