# encoding: utf-8
from layer_searcher import create_str_polygon_postgis
from utils import parseUserTextInput;


def getTsTextQuery(query_object):
	#query object fields : text, polygon, startDate, endDate
	params = []
	qs = 'SELECT "timeSeries_variable"."id", "timeSeries_variable"."name", "timeSeries_station"."id" '
	qs = qs + 'from "timeSeries_variable", "timeSeries_stationtype", "timeSeries_station", "timeSeries_stationtype_variables" '
	qs = qs +'WHERE "timeSeries_station"."stationType_id" = "timeSeries_stationtype"."id" AND '
	qs = qs + '"timeSeries_stationtype"."id" = "timeSeries_stationtype_variables"."stationtype_id" AND '
	qs = qs + '"timeSeries_stationtype_variables"."variable_id" = "timeSeries_variable"."id" '
	if(query_object.has_key("bbox")):
		bbox_str = create_str_polygon_postgis(query_object["bbox"])
		if bbox_str == None:
			return "Error"
		qs = qs + 'AND ST_Intersects("timeSeries_station"."location", %s)'
		params.append(bbox_str)

	if(query_object.has_key("ini") and query_object.has_key("end")):
		""" startDate and endDate are datetime instances
		"""
		startDateStr = query_object["ini"].strftime("%Y-%m-%d %H:%M:%S")
		endDateStr = query_object["end"].strftime("%Y-%m-%d %H:%M:%S")
		qs = qs + 'AND "timeSeries_station"."id" in ( SELECT "timeSeries_measurements"."idStation" FROM "timeSeries_measurements" WHERE %s <= "timeSeries_measurements"."ts" AND %s >= "timeSeries_measurements"."ts" ) '
		params.append(startDateStr)
		params.append(endDateStr)
	if(query_object.has_key("text") or query_object.has_key("categories") ):
		#check if the user entered a text or categories to the search
		text = query_object.get("text","")
		categories = query_object.get("categories", [])
		if(text or len(categories)>0):
			ts_query_str = parseUserTextInput(text,categories);
			qs = qs + 'AND "timeSeries_variable"."ts_index" @@ to_tsquery(\'spanish\', %s) '
			params.append(ts_query_str)
	qs = qs + 'LIMIT 10;'
	print("EL QUERY DE BUSQUEDA  "+ qs)
	return qs, params


