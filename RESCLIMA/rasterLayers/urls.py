
from django.conf.urls import patterns, url

urlpatterns = patterns('rasterLayers.views',
	url(r'^$','list_rasterlayers',name='raster_list'),
	url(r'^import$', 'import_raster'),
	url(r'^view/(?P<rasterlayer_id>\d+)$', 'view_raster'),
	url(r'^edit/(?P<rasterlayer_id>\d+)$', 'edit_raster'),
	# estilos
	url(r'^import_style$', 'import_style', name="import_style"),
	url(r'^delete_style/(?P<style_id>\d+)$', 'delete_style', name="delete_style"),
	url(r'^export_style/(?P<style_id>\d+)$','export_style'),
)
