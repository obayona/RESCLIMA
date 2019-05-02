from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    url(r'^trackpoints/$', login_required(view_tracks,login_url='noAccess'), name='tracks_views'),
    url(r'^create/$', login_required(TrackFileCreate.as_view(), login_url='noAccess'), name='trackfile_create'),
    url(r'^$', login_required(TrackFileList.as_view(), login_url='noAccess'), name='trackfile_list'),
    url(r'^update/(?P<pk>\d+)/$', login_required(TrackFileUpdate.as_view(), login_url='noAccess'), name='trackfile_update'),
    url(r'^delete/(?P<pk>\d+)/$', login_required(TrackFileDelete.as_view(), login_url='noAccess'), name='trackfile_delete'),
    url(r'^trackpoints/(?P<id_sensor>\w+)/(?P<date_init>[-\w]+)/(?P<date_end>[-\w]+)/$', track_files_generator, name='tracks_generator'),
    url(r'^trackpoints/info/(?P<id_sensor>\w+)/$',get_info_sensor),
    url(r'^gpxfile/(?P<id_sensor>\w+)/(?P<date_init>[-\w]+)/(?P<date_end>[-\w]+)/$',track_files_viewer),
    url(r'^metadata/(?P<id_sensor>\w+)/(?P<date_init>[-\w]+)/(?P<date_end>[-\w]+)/$',getmetadata_gpx, name='metadata_view'),
]
