from django.conf.urls import patterns, url

urlpatterns = patterns('VectorLayers.views',
	url(r'^$','list_vectorlayers',name="vector_list"),
	url(r'^import$', 'import_shapefile'),
	url(r'^export/(?P<vectorlayer_id>\d+)$', 'export_shapefile'),
	url(r'^geojson/(?P<vectorlayer_id>\d+)$', 'export_geojson'),
	url(r'^view/(?P<vectorlayer_id>\d+)$', 'view_vectorlayer'),
	url(r'^edit/(?P<vectorlayer_id>\d+)$', 'edit_vectorlayer'),
	# estilos
	url(r'^import_style/(?P<vectorlayer_id>\d+)$', 'import_style', name="import_style"),
	url(r'^delete_style/(?P<style_id>\d+)$', 'delete_style', name="delete_style"),
	url(r'^export_style/(?P<style_id>\d+)$','export_style'),
)
