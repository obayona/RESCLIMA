from django.conf.urls import url
from search.views import search_layer

urlpatterns =[
	url(r'^layer/$', search_layer),
]
