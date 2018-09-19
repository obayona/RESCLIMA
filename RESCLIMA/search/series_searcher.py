# encoding: utf-8
from layer_searcher import create_str_polygon_postgis

def getTsTextQuery(query_object):
	#query object fields : text, polygon, startDate, endDate
	params = []
	qs = 'SELECT "timeSeries_variable"."id", "timeSeries_variable"."name", "timeSeries_station"."id" '
	qs = qs + 'from "timeSeries_variable", "timeSeries_stationtype", "timeSeries_station", "timeSeries_stationtype_variables" '
	qs = qs +'WHERE "timeSeries_station"."stationType_id" = "timeSeries_stationtype"."id" AND '
	qs = qs + '"timeSeries_stationtype"."id" = "timeSeries_stationtype_variables"."stationtype_id" AND '
	qs = qs + '"timeSeries_stationtype_variables"."variable_id" = "timeSeries_variable"."id" AND '
	if(query_object.has_key("bbox")):
		bbox_str = create_str_polygon_postgis(query_object["bbox"])
		if bbox_str == None:
			return "Error"
		qs = qs + 'ST_Intersects("timeSeries_station"."location", %s)'
		params.append(bbox_str)

	if(query_object.has_key("ini_date") and query_object.has_key("end_date")):
		""" startDate and endDate are datetime instances
		"""
		startDateStr = query_object["ini_date"].strftime("%Y-%m-%d %H:%M:%S")
		endDateStr = query_object["end_date"].strftime("%Y-%m-%d %H:%M:%S")
		qs = qs + 'AND "timeSeries_station"."id" in ( SELECT "timeSeries_measurements"."idStation" FROM "timeSeries_measurements" WHERE %s <= "timeSeries_measurements"."ts" AND %s >= "timeSeries_measurements"."ts" ) '
		params.append(startDateStr)
		params.append(endDateStr)
	if(query_object.has_key("text")):
		qs = qs + 'AND "timeSeries_variable"."ts_index" @@ to_tsquery(\'spanish\', %s) '
		params.append(query_object["text"])
	qs = qs + 'LIMIT 10;'
	print("EL QUERY DE BUSQUEDA  "+ qs)
	return qs, params

""""def getStationsVariables(text):
	variableStations = []
	qs, params = getTsTextQuery(text)
	with connection.cursor() as cursor:
		cursor.execute(qs, params)
		rows = cursor.fetchall()
		for row in rows:
			variableStation = {}
			variableStation['id_station'] = row[0]
			variableStation['name'] = row[1]
			variableStation['id_variable'] = row[2]
			variableStations.append(variableStation)
	return variableStations"""
