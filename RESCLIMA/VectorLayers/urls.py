from django.conf.urls import patterns, url

urlpatterns = patterns('VectorLayers.views',
	url(r'^$','list_vectorlayers'),
	url(r'^import$', 'import_shapefile'),
	url(r'^export/(?P<vectorlayer_id>\d+)$', 'export_shapefile'),
	url(r'^geojson/(?P<vectorlayer_id>\d+)$', 'export_geojson'),
	url(r'^view/(?P<vectorlayer_id>\d+)$', 'view_vectorlayer'),
	url(r'^edit/(?P<vectorlayer_id>\d+)$', 'edit_vectorlayer'),
)