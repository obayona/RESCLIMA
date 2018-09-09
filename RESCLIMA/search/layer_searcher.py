# encoding: utf-8


def create_str_polygon_postgis(polygon_dict):
	minX = polygon_dict["minX"];
	maxX = polygon_dict["maxX"];
	minY = polygon_dict["minY"];
	maxY = polygon_dict["maxY"];
	if (minX=='0' and maxX=='0' and minY=='0' and maxY=='0'):
		return None
	else:
		polygon_str = "SRID=4326;POLYGON((%s %s,%s %s,%s %s,%s %s,%s %s))::geometry"%(float(minX),float(minY),float(minX),float(maxY),float(maxX),float(maxY),float(maxX),float(minY),float(minX),float(minY));
		return polygon_str


def appendQueryPart(query,query_part, separator):
	return query + separator + query_part

# Genera un query dinamico depenciendo
# de las opciones de query_object
def create_query(query_object):
	# TODO: validar si es vacio
	
	# sql statements
	select_stm = 'SELECT l.id, l.title, l.abstract, l.type, l.bbox';
	categories = []
	if query_object.has_key("categories"):
		categories = query_object["categories"]

	if len(categories)>0:
		from_stm = 'FROM "layer_layer" AS l, "layer_layer_categories" AS lc,"search_category" AS c';
	else:
		from_stm = 'FROM "layer_layer" AS l';
	where_stm = 'WHERE';
	where_filters = [];
	params = []
	# opciones de busqueda
	text = None
	bbox = None
	categories = []
	end_date = None
	ini_date = None

	if(query_object.has_key("text")):
		filter_str = 'ts_index @@ plainto_tsquery(\'spanish\',%s)'
		where_filters.append(filter_str);
		params.append(query_object["text"]);

	if(len(categories)>0):
		filter_str = "l.id = lc.layer_id and c.id=lc.category_id and ("
		for i,category in enumerate(categories):
			part_str = "c.id = %s";
			params.append(category);
			if (i==0):
				filter_str = filter_str + part_str;
			else:
				filter_str = filter_str + " or " + part_str;
		filter_str = filter_str + ")";
		where_filters.append(filter_str)


	if(query_object.has_key("bbox")):
		bbox_str = create_str_polygon_postgis(query_object["bbox"]);
		if bbox_str == None:
			return "Error";
		filter_str = 'ST_Intersects(bbox,%s)';
		where_filters.append(filter_str);
		params.append(bbox_str);

	if(query_object.has_key("ini_date") and query_object.has_key("end_date")):
		filter_str = 'data_date >= %s and data_date <= %s';
		where_filters.append(filter_str)
		params.append(query_object["ini_date"]);
		params.append(query_object["end_date"]);


	sql_query = select_stm;
	sql_query = appendQueryPart(sql_query,from_stm," ");
	sql_query = appendQueryPart(sql_query,where_stm," ");

	for i,f in enumerate(where_filters):
		if (i==0):
			sql_query = appendQueryPart(sql_query,f," ");
		else:
			sql_query = appendQueryPart(sql_query,f," and ");


	return sql_query, params

