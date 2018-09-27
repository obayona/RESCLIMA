# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from os.path import join
from forms import ImportRasterForm
from forms import ImportStyleForm
from RESCLIMA import settings
from models import RasterLayer
from style.models import Style
import datetime
import time
import importer
from search.models import Category
from style.utils import transformSLD
from style.utils import getColorMap
import json

def list_rasterlayers(request):
	rasterlayers = RasterLayer.objects.all().order_by("upload_date");
	styles = Style.objects.filter(type="raster");
	obj = {'rasterlayers':rasterlayers,'styles':styles}
	return render(request,"list_rasterlayers.html",obj)

def import_raster(request):
	if request.method == "GET":
		categories = Category.objects.all();
		return render(request, "import_raster.html",{'categories':categories})
	elif request.method == "POST":
		result = {}
		try:
			print "se ejecuta la tarea en import_raster"
			result = importer.import_data(request)
			print "el resultado de la tarea en import_raster", result
			return HttpResponse(json.dumps(result),content_type='application/json')
		except Exception as e:
			print "El error en import_raster", e
			result["error"]=str(e);
			return HttpResponse(json.dumps(result),content_type='application/json')


def view_raster(request,rasterlayer_id):
	try:
		rasterlayer = RasterLayer.objects.get(id=rasterlayer_id)
		bbox = rasterlayer.bbox.geojson
		# se comprueba si tiene estilo
		layer_styles = Style.objects.filter(layers__id=rasterlayer_id)
		legend = [];
		if layer_styles.count()==1:
			style = layer_styles[0]
			legend = getColorMap(style);

	except RasterLayer.DoesNotExist:
		return HttpResponseNotFound()

	obj = {"rasterlayer":rasterlayer,
		"bbox":bbox,
		"legend":legend}

	return render(request,"view_raster.html",obj)


def updateRasterLayer(rasterlayer,request):
	try:
		title = request.POST["title"]
		abstract = request.POST["abstract"]
		id_style = request.POST["style"]
		if(title=="" or abstract==""):
			return "Error en el formulario"

		rasterlayer.title = title;
		rasterlayer.abstract = abstract;
		rasterlayer.save()
		if id_style != "null":
			style = Style.objects.get(id=id_style)
			style.layers.add(rasterlayer)
			style.save()
		else:
			rasterlayer.style_set.clear()
	except Exception as e:
		return "Error " + str(e)


def edit_raster(request, rasterlayer_id):
    try:
        rasterlayer = RasterLayer.objects.get(id=rasterlayer_id)
    except RasterLayer.DoesNotExist:
        return HttpResponseNotFound()

    styles = Style.objects.filter(type="raster")
    layer_styles = Style.objects.filter(layers__id=rasterlayer_id)
    layer_style_id = None
    if layer_styles.count()==1:
        layer_style = layer_styles[0]
        layer_style_id = layer_style.id

    if request.method == "GET":
        params = {"rasterlayer":rasterlayer,
                  "styles":styles,
                  "layer_style_id":layer_style_id,
                  "err_msg":None}
        return render(request,"update_rasterlayer.html",params)

    elif request.method == "POST":
        err_msg = updateRasterLayer(rasterlayer,request)
        if(err_msg==None):
            return HttpResponseRedirect("/raster")

    params = {"rasterlayer":rasterlayer,
              "styles":styles,
              "layer_style_id":layer_style_id,
              "err_msg":err_msg}
    return render(request,"update_rasterlayer.html",params)  


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
    f = open(fullName,'w');
    f.write(sld_string);
    f.close();

    style = Style(file_path=path,file_name=fileName,
      title=title, type="raster");
    style.save()
  except Exception as e:
    return "Error " + str(e)


def import_style(request):

  if request.method == "GET":
    form = ImportStyleForm()
    return render(request,"import_style.html",{"form":form});

  if request.method == "POST":
    err_msg = None
    form = ImportStyleForm(request.POST,request.FILES)
    if form.is_valid():
      err_msg = importStyle(request)
      if(err_msg==None):
        return HttpResponseRedirect("/raster")

    params = {"form":form,"err_msg":err_msg}
    return render(request,"import_style.html",params) 

def delete_style(request,style_id):
  try:
    style = Style.objects.get(id=style_id)
    style.delete();
    return HttpResponse("OK");
  except Style.DoesNotExist:
    return HttpResponseNotFound()  

def export_style(request,style_id):
  try:
    style = Style.objects.get(id=style_id)
    file_path = style.file_path;
    file_name = style.file_name;
    fullName = join(file_path,file_name);
    f = open(fullName,'r');
    sld = f.read()
    return HttpResponse(sld)
  except Exception as e:
    print e
    return HttpResponseNotFound()


