# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from forms import ImportGeotiffForm
import importer

def list_rasterlayers(request):
	return HttpResponse("Lista de Rasters");

def import_geotiff(request):
    if request.method == "GET":
        form = ImportGeotiffForm()
        return render(request, "import_geotiff.html",{'form':form})
    elif request.method == "POST":
        form = ImportGeotiffForm(request.POST,request.FILES)
        if form.is_valid():
            err_msg = importer.import_data(request)
            if err_msg == None:
                return HttpResponse("OK")
            else:
                err_msg = "Error en el formulario"
            return HttpResponse(err_msg);


def view_geotiff(request):
    return render(request,"view_geotiff.html")
