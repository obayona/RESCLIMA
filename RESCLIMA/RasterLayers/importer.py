# -*- encoding: utf-8 -*-

import os, os.path
import datetime
import time
import requests


def import_data(request):
	list_files = request.FILES.getlist('import_files')
	title = request.POST["title"]
	abstract = request.POST["abstract"]

	# se guarda el archivo en una carpeta
	file_dir = None
	fileName = None
	for file in list_files:
		fileName = file.name.split(".")[0];
		ts = time.time()
		timestamp_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
		fileName = fileName + timestamp_str + ".tif" 
		print fileName
		file_dir = os.path.join("/home_local/obayona/rasters",fileName)
		f = open(file_dir, 'wb+')	
		for chunk in file.chunks():
			f.write(chunk)
		f.close()

	return None

"""
	ts = time.time()
	timestamp_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
	# se crea el coverage store en geoserver
	url = "http://localhost:8080/geoserver/rest/workspaces/resclima_raster/coveragestores?configure=all"
	auth = ("admin","geoserver")
	headers = {"Content-type":"text/xml"}
	xml = open("/home_local/obayona/RESCLIMA/RESCLIMA/RasterLayers/xml/coverage.xml","r");
	data = xml.read()
	coverage_name = "covergare"+timestamp_str
	data = data.replace("{%name%}",coverage_name)
	data = data.replace("{%workspace%}","resclima_raster")
	data = data.replace("{%url%}",file_dir)
	
	print data, url
	resp = requests.post(url,headers=headers,data=data,auth=auth);
	print "respuesta",resp.status_code, resp.content


	# se crea la capa en geoserver
	url = "http://localhost:8080/geoserver/rest/workspaces/resclima_raster/coveragestores/"+coverage_name+"/coverages"
	xml = open("/home_local/obayona/RESCLIMA/RESCLIMA/RasterLayers/xml/layer.xml","r")
	data = xml.read()
	layer_name = fileName.replace(".tif","");
	data = data.replace("{%name%}",layer_name)
	data = data.replace("{%title%}",title)
	print data, url
	resp = requests.post(url,headers=headers,data=data,auth=auth);	
	print resp.status_code, resp.content

"""