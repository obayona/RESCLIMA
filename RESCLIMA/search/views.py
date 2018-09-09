# encoding: utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
from django.core.paginator import Paginator
from django.contrib.gis.geos import Polygon

def create_query(text, polygon):
	qs = ''
	params = []
	#QUERY SOLO TEXTO
	if (polygon==None):
		qs = 'SELECT id, title, abstract, type, bbox, ts_rank_cd(textsearchable_index, query)' 
		qs = qs + ' AS rank FROM "layer_layer", plainto_tsquery(\'spanish\',%s)'
		qs = qs + ' query WHERE query @@ textsearchable_index'
		qs = qs + ' ORDER BY rank DESC LIMIT 10'
		params.append(text)
		return qs, params
	
	#QUERY SOLO BBOX
	elif (text==''):
		qs = 'SELECT id, title, abstract, type, bbox' 
		qs = qs + ' FROM "layer_layer"'
		qs = qs + ' WHERE ST_Intersects(bbox,%s)'
		qs = qs + ' LIMIT 10'
		params.append(polygon)
		return qs, params
	
	#QUERY TEXTO Y BBOX
	else:
		qs = 'SELECT id, title, abstract, type, bbox, ts_rank_cd(textsearchable_index, query)' 
		qs = qs + ' AS rank FROM "layer_layer", plainto_tsquery(\'spanish\',%s)'
		qs = qs + ' query WHERE query @@ textsearchable_index AND ST_Intersects(bbox,%s)'
		qs = qs + ' ORDER BY rank DESC LIMIT 10'
		params.append(text)
		params.append(polygon)
		return qs, params


def create_polygon(minX, maxX, minY, maxY):
	if (minX=='0' and maxX=='0' and minY=='0' and maxY=='0'):
		return None
	else:
		polygon_str = "SRID=4326;POLYGON((%s %s,%s %s,%s %s,%s %s,%s %s))::geometry"%(float(minX),float(minY),float(minX),float(maxY),float(maxX),float(maxY),float(maxX),float(minY),float(minX),float(minY));
		return polygon_str

def search_layer(request):
	minX = request.GET["left"];
	maxX = request.GET["right"];
	minY = request.GET["bottom"];
	maxY = request.GET["top"];
	user_query = request.GET["q"];
	user_polygon = create_polygon(minX,maxX,minY,maxY)
	qs,params = create_query(user_query, user_polygon)
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

def getTsTextQuery(text):
	qs = 'SELECT "timeSeries_variable"."id", "timeSeries_station"."id" '
	qs = qs + 'from "timeSeries_variable", "timeSeries_stationtype", "timeSeries_station", "timeSeries_stationtype_variables" '
	qs = 'WHERE "timeSeries_station"."stationType_id" = "timeSeries_stationtype"."id" AND '
	qs = qs + '"timeSeries_stationtype"."id" = "timeSeries_stationtype_variables"."stationtype_id" AND '
	qs = qs + '"timeSeries_stationtype_variables"."variable_id" = "timeSeries_variable"."id" AND '
	qs = qs + '"timeSeries_variable"."ts_index" @@ plainto_tsquery("spanish", %s) '
	qs = qs + 'LIMIT 10;'
	params = [text]
	return qs, params

def getStationsVariables(text):
	variableStations = []
	qs, params = getTsTextQuery(text)
	with connection.cursor() as cursor:
		cursor.execute(qs, params)
		rows = cursor.fetchall()
		for row in rows:
			variableStation = {}
			variableStation['id_station'] = row[0]
			variableStation['id_variable'] = row[1]
			variableStations.append(variableStation)
	return variableStations

	def filterStationsInBbox(variableStations, polygon):
		filtVariableStations = []
		if (polygon == None):
			return variableStations
		for variableStations 
		


and ST_interset(Station.bbox,"%bbox_user") // filtrando las estaciones que estan dentro del bbox
and exitst(select * from measuement where station.id_station == masuement.id_station and ts > %inicial_date) and exist(select * from measuement where station.id_station == masuement.id_station and ts < %final_date) // validar las fechas


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
