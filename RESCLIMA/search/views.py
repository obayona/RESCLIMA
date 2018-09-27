# encoding: utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
from django.core.paginator import Paginator
from models import Category
import json
import layer_searcher, series_searcher

def categories_json(request):
	categories = Category.objects.all()
	result = []
	for category in categories:
		result.append({"id":category.id,
			      "name":category.name,
			      "selected":False})

	result_json = json.dumps({"categories":result});
	return HttpResponse(result_json,content_type='application/json')
			


def search_layer(request):
	query_str = request.body;
	query_dict = json.loads(query_str)
	print "el query de busqueda ******",query_dict
	qs,params = layer_searcher.create_query(query_dict)
	layers = []
	with connection.cursor() as cursor:
		cursor.execute(qs, params)
		rows = cursor.fetchall()
		for row in rows:
			layer = {}
			layer["id"] = row[0];
			layer["title"] = row[1];
			layer["abstract"] = row[2];
			layer["type"] = row[3];
			layer["selected"] = False;
			layers.append(layer)
	print layers
	return JsonResponse({"results":layers})

def search_series(request):
	#PONER COMO DESCRIPCION NUMERO DE ESTACIONES
	query_str = request.body;
	query_dict = json.loads(query_str)
	print "el diccionario de busqueda ******",query_dict
	qs,params = series_searcher.getTsTextQuery(query_dict)
	series = []
	variablesStations = {}
	with connection.cursor() as cursor:
		cursor.execute(qs, params)
		rows = cursor.fetchall()
		for row in rows:
			#first we have to group by variable id the stations that measure that variable
			if(variablesStations.has_key(row[2])):
				variablesStations[row[2]]["stations_ids"].append(row[0])
			else:
				serieData={}
				serieData["variable_id"] = row[0]
				serieData["variable_name"] = row[1]
				serieData["stations_ids"] = []
				serieData["stations_ids"].append(row[2])
				serieData["selected"] = False
				variablesStations[row[0]] = serieData
	#we then push to an array
	for id in variablesStations.keys():
		variablesStations[id]['amount_stations'] = len(variablesStations[id]['stations_ids'])
		series.append(variablesStations[id])
	return JsonResponse({"results":series})




"""
PARAMETROS:
request: Request de la vista
queryset: Queryset a utilizar en la paginacion
pages: Numero de items que quisieras tener en cada pagina
"""
def Paginate(request, queryset, pages):
	# Retorna el objeto paginator para comenzar el trabajo
	result_list = Paginator(queryset, pages)
 
	try:
		# Tomamos el valor de parametro page, usando GET
		page = int(request.GET.get('page'))
	except:
		page = 1
 
	# Si es menor o igual a 0 igualo en 1
	if page <= 0:
		page = 1
 
	# Si viene un parametro que es mayor a la cantidad
	# de paginas le igualo el parámetro con las cant de paginas
	if(page > result_list.num_pages):
		page = result_list.num_pages
 
	# Verificamos si esta dentro del rango
	if (result_list.num_pages >= page):
		# Obtengo el listado correspondiente al page
		pagina = result_list.page(page)
 
		context = {
			'queryset': pagina.object_list,
			'page': page,
			'pages': result_list.num_pages,
			'has_next': pagina.has_next(),
			'has_prev': pagina.has_previous(),
			'next_page': page+1,
			'prev_page': page-1,
			'firstPage': 1,
		}
 
	return context

