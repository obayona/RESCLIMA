# encoding: utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
from django.core.paginator import Paginator
import json
import layer_searcher


def search_layer(request):
	print request.body
	query_str = request.body;
	query_dict = json.loads(query_str)
        print query_dict
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
			layers.append(layer)

	return JsonResponse({"layers":layers})

def getTsTextQuery(text);
	qs = 'SELECT "timeSeries_variable"."id", "timeSeries_station"."id" '
	qs = qs + 'from "timeSeries_variable", "timeSeries_stationtype", "timeSeries_station", "timeSeries_stationtype_variables" '
	qs = 'WHERE "timeSeries_station"."stationType_id" = "timeSeries_stationtype"."id" AND '
	qs = qs + '"timeSeries_stationtype"."id" = "timeSeries_stationtype_variables"."stationtype_id" AND '
	qs = qs + '"timeSeries_stationtype_variables"."variable_id" = "timeSeries_variable"."id" AND '
	qs = qs + '"timeSeries_variable"."ts_index" @@ plainto_tsquery("spanish", %s);'
	params = [text]
	return qs, params

def getStationsVariables(text):
	variableStationSet = set()
	qs, params = getTsTextQuery(text)
	with connection.cursor() as cursor:
		cursor.execute(qs, params)
		rows = cursor.fetchall()
		for row in rows:
			variableStation = {}
			variableStation['id_station'] = row[0]
			variableStation['id_variable'] = row[1]
			variableStationSet.add(variableStation)

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

