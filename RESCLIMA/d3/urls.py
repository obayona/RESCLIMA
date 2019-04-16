from django.conf.urls import url
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns =[
    url(r'^api/test$', test, name='test'),
    url(r'^logistica/dashboard/$', login_required(logistica), name='logistica_dash'), 
    url(r'^clima/dashboard/$', login_required(clima), name='logistica_dash'),
    url(r'^poblacion/dashboard/$', login_required(poblacion), name='logistica_dash'),

]
