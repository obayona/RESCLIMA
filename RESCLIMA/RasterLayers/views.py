# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from os.path import join
from forms import ImportRasterForm
from forms import ImportStyleForm
from RESCLIMA import settings
from models import RasterLayer, Style
import datetime
import time
import importer
import utils
import json


def list_rasterlayers(request):
    rasterlayers = RasterLayer.objects.all().order_by("upload_date");
    styles = Style.objects.all();
    obj = {'rasterlayers':rasterlayers,'styles':styles}
    return render(request,"list_rasterlayers.html",obj)

def import_raster(request):
    if request.method == "GET":
        form = ImportRasterForm()
        return render(request, "import_raster.html",{'form':form})
    elif request.method == "POST":
        form = ImportRasterForm(request.POST,request.FILES)
        if form.is_valid():
            err_msg = importer.import_data(request)
        else:
            err_msg = form.errors;
        if err_msg == None:
            return HttpResponse("OK")
        else:
            return HttpResponse(err_msg);


def view_raster(request,rasterlayer_id):
    try:
        rasterlayer = RasterLayer.objects.get(id=rasterlayer_id)
        bbox = rasterlayer.bbox.geojson
        bbox = json.dumps(bbox)
        print bbox
    except RasterLayer.DoesNotExist:
        return HttpResponseNotFound()

    obj = {"rasterlayer":rasterlayer,
           "bbox":bbox}
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
        if id_style != "null":
            rasterlayer.style = Style.objects.get(id=id_style)
        else:
            rasterlayer.style = None;
        rasterlayer.save()
    except Exception as e:
        return "Error " + str(e)


def edit_raster(request, rasterlayer_id):
    try:
        rasterlayer = RasterLayer.objects.get(id=rasterlayer_id)
    except RasterLayer.DoesNotExist:
        return HttpResponseNotFound()

    styles = Style.objects.all()

    if request.method == "GET":
        params = {"rasterlayer":rasterlayer,
                  "styles":styles,
                  "err_msg":None}
        return render(request,"update_rasterlayer.html",params)

    elif request.method == "POST":
        err_msg = updateRasterLayer(rasterlayer,request)
        if(err_msg==None):
            return HttpResponseRedirect("/raster")

    params = {"rasterlayer":rasterlayer,
              "styles":styles,
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
    sld_string = utils.transformSLD(sld_string);

    f.close();
    f = open(fullName,'w');
    f.write(sld_string);
    f.close();

    style = Style(file_path=path,file_name=fileName,
      title=title);
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