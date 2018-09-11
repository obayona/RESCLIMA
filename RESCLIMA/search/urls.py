from django.conf.urls import url
from search.views import search_layer,categories_json

urlpatterns =[
	url(r'^layer/$', search_layer),
	url(r'^categories/$', categories_json),
]
