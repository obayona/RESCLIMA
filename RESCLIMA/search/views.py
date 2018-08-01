# encoding: utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
from django.core.paginator import Paginator
from django.contrib.gis.geos import Polygon

def search_layer(request):

	user_query = request.GET["q"];

	qs = 'SELECT id, title, abstract, type, bbox ts_rank_cd(textsearchable_index, query)' 
	qs = qs + ' AS rank FROM "Layer_layer", plainto_tsquery(\'spanish\',%s)'
	qs = qs + ' query WHERE query @@ textsearchable_index'
	qs = qs + ' ORDER BY rank DESC LIMIT 10'

    #Text Search
	layers = []
	with connection.cursor() as cursor:
		cursor.execute(qs, [user_query])
		rows = cursor.fetchall()
		for row in rows:
			layer = {}
			layer["id"] = row[0];
			layer["title"] = row[1];
			layer["abstract"] = row[2];
			layer["type"] = row[3];
            layer["bbox"] = row[4];
			layers.append(layer)

    #Bbox Search
    minX = request.GET["left"];
    maxX = request.GET["right"];
    minY_query = request.GET["bottom"];
    maxY = request.GET["top"];
    box = Polygon( ((minX, minY), (minX, maxY), (maxX, minY), (maxX, maxY), srid=4326))

    finalLayers = []
    for layer in layers:
        layerBox = layer["bbox"]
        qb = 'SELECT ST_Intersects(box, bbox)'
        if (qb):
            finalLayers.append(layer)


	return JsonResponse({"layers":finalLayers})

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