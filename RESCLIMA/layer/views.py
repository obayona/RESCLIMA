# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from models import Layer
import json

def view_layers(request):
	return render(request,"view_layers.html")

def layer_info(request,id_layer):
	layer = Layer.objects.get(id=id_layer)
	layer_json = {}
	layer_json["id"]=id_layer
	layer_json["title"]=layer.title
	layer_json["abstract"]=layer.abstract
	layer_json["type"]=layer.type
	data_date_str = str(layer.data_date)
	data_date_str = data_date_str.replace("-","/")
	layer_json["data_date"]=data_date_str
	#bbox
	return HttpResponse(json.dumps(layer_json),content_type='application/json')
	
