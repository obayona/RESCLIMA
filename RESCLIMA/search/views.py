from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection

def search_layer(request):

	user_query = request.GET["q"];

	qs = 'SELECT id, title, abstract, type, ts_rank_cd(textsearchable_index, query)' 
	qs = qs + ' AS rank FROM "Layer_layer", plainto_tsquery(\'spanish\',%s)'
	qs = qs + ' query WHERE query @@ textsearchable_index'
	qs = qs + ' ORDER BY rank DESC LIMIT 10'

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
			layers.append(layer)

	return JsonResponse({"layers":layers})
