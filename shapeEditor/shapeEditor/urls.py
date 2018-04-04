from django.conf.urls import include, url
from django.contrib.gis import admin


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^editor/',include('shapeEditor.editor.urls')),
]
