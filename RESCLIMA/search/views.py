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
	return JsonResponse({"results":[]})


def getTsTextQuery(text, polygon, startDate, endDate):
	params = []
	qs = 'SELECT "timeSeries_variable"."id", "timeSeries_variable"."name", "timeSeries_station"."id" '
	qs = qs + 'from "timeSeries_variable", "timeSeries_stationtype", "timeSeries_station", "timeSeries_stationtype_variables" '
	qs = 'WHERE "timeSeries_station"."stationType_id" = "timeSeries_stationtype"."id" AND '
	qs = qs + '"timeSeries_stationtype"."id" = "timeSeries_stationtype_variables"."stationtype_id" AND '
	qs = qs + '"timeSeries_stationtype_variables"."variable_id" = "timeSeries_variable"."id" AND '
	if polygon != None:
		qs = qs + 'ST_Intersects("timeSeries_station"."location", %s) AND '
		params.append(polygon)
	if startDate != None and endDate != None:
		""" startDate and endDate are datetime instances
		"""
		startDateStr = startDate.strftime("%Y-%m-%d %H:%M:%S")
		endDateStr = endDate.strftime("%Y-%m-%d %H:%M:%S")
		qs = qs + '"timeSeries_station"."id" in ( SELECT "timeSeries_measurements"."idStation" FROM "timeSeries_measurements" WHERE %s <= "timeSeries_measurements"."ts" AND %s >= "timeSeries_measurements"."ts" ) AND '
		params.append(startDateStr)
		params.append(endDateStr)
	qs = qs + '"timeSeries_variable"."ts_index" @@ to_tsquery(\'spanish\', %s) '
	qs = qs + 'LIMIT 10;'
	params.append(text)
	return qs, params

def getStationsVariables(text):
	variableStations = []
	qs, params = getTsTextQuery(text)
	with connection.cursor() as cursor:
		cursor.execute(qs, params)
		rows = cursor.fetchall()
		for row in rows:
			variableStation = {}
			variableStation['id_variable'] = row[0]
			variableStation['name_variable'] = row[1]
			variableStation['id_station'] = row[2]
			variableStations.append(variableStation)
	return JsonResponse({"variableStations":variableStations})

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

