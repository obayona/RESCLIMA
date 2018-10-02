
from django.conf.urls import url
from rasterLayers import views as rasterLayers_views

urlpatterns =[
	url(r'^$', rasterLayers_views.list_rasterlayers,name='raster_list'),
	url(r'^import$', rasterLayers_views.import_raster),
	url(r'^view/(?P<rasterlayer_id>\d+)$', rasterLayers_views.view_raster),
	url(r'^edit/(?P<rasterlayer_id>\d+)$', rasterLayers_views.edit_raster),
	url(r'^delete/(?P<rasterlayer_id>\w+)/$$', rasterLayers_views.delete_rasterLayer, name="delete_layer"),
	# estilos
	url(r'^import_style$', rasterLayers_views.import_style, name="import_style"),
	url(r'^delete_style/(?P<style_id>\d+)$', rasterLayers_views.delete_style, name="delete_style"),
	url(r'^export_style/(?P<style_id>\d+)$', rasterLayers_views.export_style),
]
