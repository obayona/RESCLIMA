# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from main.models import Researcher
import os
from os.path import join
import rasterLayers.importer as importer
from rasterLayers.models import RasterLayer
from RESCLIMA import settings
from search.models import Category
import simplejson as json
from style.models import Style
from style.utils import transformSLD,getColorMap,loadStyle, removeStyle
import time
from wsgiref.util import FileWrapper


limit = 10
@login_required(login_url='noAccess')
def list_rasterlayers(request):
	researcher = request.user.researcher
	researcher = researcher.id
	layers = RasterLayer.objects.filter(owner=researcher).order_by("-upload_date")
	styles = Style.objects.filter(type="raster", owner=researcher)
	page = request.GET.get('page', 1)
	paginator1 = Paginator(layers, limit)
	try:
		rasterlayers = paginator1.page(page)
	except PageNotAnInteger:
		rasterlayers = paginator1.page(1)
	except EmptyPage:
		rasterlayers = paginator1.page(paginator1.num_pages)
	obj = {'rasterlayers':rasterlayers,'styles':styles}
	return render(request,"list_rasterlayers.html",obj)

@login_required(login_url='noAccess')
@csrf_protect
def import_raster(request):
	if request.method == "GET":
		categories = Category.objects.all();
		return render(request, "import_raster.html",{'categories':categories})
	elif request.method == "POST":
		result = {}
		try:
			result = importer.import_data(request)
			return HttpResponse(json.dumps(result),content_type='application/json')
		except Exception as e:
			result["error"]=str(e);
			return HttpResponse(json.dumps(result),content_type='application/json')


def export_rasterLayer(request,rasterlayer_id):
	rasterlayer = RasterLayer.objects.get(id=rasterlayer_id)
	file_path = rasterlayer.file_path
	file_name = rasterlayer.file_name
	fullName = join(file_path,file_name)

	f = FileWrapper(open(fullName,"rb"))
	response = HttpResponse(f, content_type="image/tiff")
	response['Content-Disposition'] = "attachment; filename=" + file_name
	return response

def style_legend(request,style_id):
	style = Style.objects.get(id=style_id)
	legend = getColorMap(style);
	return HttpResponse(json.dumps(legend),content_type='application/json')

def updateRasterLayer(rasterlayer,request):
	try:
		title = request.POST["title"]
		abstract = request.POST["abstract"]
		author = request.POST["author"]
		id_style = request.POST["style"]
		date_str = request.POST["data_date"] # fecha como string
		# fecha como objeto datetime
		data_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
		categories_string = request.POST["categories_string"]

		rasterlayer.title = title
		rasterlayer.abstract = abstract
		rasterlayer.author = author
		rasterlayer.data_date = data_date
		rasterlayer.categories_string = categories_string
		rasterlayer.save()

		# se actualiza el estilo
		if id_style != "null":
			style = Style.objects.get(id=id_style)
			style.layers.add(rasterlayer)
			style.save()
		else:
			rasterlayer.style_set.clear()
	except Exception as e:
		return "Error " + str(e)

@login_required(login_url='noAccess')
def edit_raster(request, rasterlayer_id):
	researcher = request.user.researcher
	researcher = researcher.id
	try:
		rasterlayer = RasterLayer.objects.get(id=rasterlayer_id)
	except RasterLayer.DoesNotExist:
		return HttpResponseNotFound()

	# se obtienen los estilos
	styles = Style.objects.filter(type="raster", owner=researcher)
	# se obtiene el estilo de la capa
	layer_styles = Style.objects.filter(layers__id=rasterlayer_id)
	layer_style_id = None
	# si se encontro un estilo
	if layer_styles.count()==1:
		layer_style = layer_styles[0]
		# se recupera el id de ese estilo
		layer_style_id = layer_style.id

	# se obtienen las categorias
	categories = Category.objects.all();

	if request.method == "GET":
		params = {"rasterlayer":rasterlayer,
				  "styles":styles,
				  "layer_style_id":layer_style_id,
				  "categories":categories}
		return render(request,"update_rasterlayer.html",params)

	elif request.method == "POST":
		err_msg = updateRasterLayer(rasterlayer,request)
		if(err_msg==None):
			return HttpResponseRedirect("/raster")
		else:
			params = {"rasterlayer":rasterlayer,
					  "styles":styles,
					  "layer_style_id":layer_style_id,
					  "categories":categories,
					  "err_msg":err_msg}
			return render(request,"update_rasterlayer.html",params)  

@login_required(login_url='noAccess')
def delete_rasterLayer(request,rasterlayer_id):
	try:
		rasterlayer = RasterLayer.objects.get(id=rasterlayer_id)
		file_path = rasterlayer.file_path
		file_name = rasterlayer.file_name
		fullName = join(file_path,file_name)
		os.remove(fullName)
		rasterlayer.delete()
		return HttpResponseRedirect("/raster")
	except RasterLayer.DoesNotExist:
		return HttpResponseNotFound()

# Styles
def importStyle(request):
	try:
		title = request.POST["title"]

		path = settings.STYLE_FILES_PATH;

		ts = time.time()
		timestamp_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
		fileName = "style_" + timestamp_str + ".sld"

		fullName = join(path,fileName)
		f = request.FILES['file']

		sld_string = f.read();
		sld_string = transformSLD(sld_string);
		f.close();
		f = open(fullName,'w',encoding="utf_8");
		f.write(sld_string);
		f.close();

		researcher = request.user.researcher
		researcher = researcher.id
		owner = Researcher.objects.get(id=researcher)
		style = Style(file_path=path,file_name=fileName,title=title, type="raster", owner=owner);
		style.save()
	except Exception as e:
		return "Error " + str(e)

@login_required(login_url='noAccess')
def import_style(request):

	if request.method == "GET":
		return render(request,"rasterLayers/import_style.html");

	if request.method == "POST":
		err_msg = importStyle(request)
		if(err_msg==None):
			return HttpResponseRedirect("/raster")
		else:
			params = {"err_msg":err_msg}
			return render(request,"rasterLayers/import_style.html",params) 

@login_required(login_url='noAccess')
def delete_style(request,style_id):
	try:
		style = Style.objects.get(id=style_id)
		removeStyle(style)
		return HttpResponseRedirect("/raster")
	except Style.DoesNotExist:
		return HttpResponseNotFound()  

def export_style(request,style_id):
	try:
		style = Style.objects.get(id=style_id)
		sld = loadStyle(style)
		return HttpResponse(sld)
	except Exception as e:
		return HttpResponseNotFound()


