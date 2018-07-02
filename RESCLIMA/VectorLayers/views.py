from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotFound, JsonResponse
from django.http import HttpResponseRedirect
from models import VectorLayer, Style
from forms import ImportShapefileForm, ImportStyleForm
import importer, exporter
from RESCLIMA import settings
import datetime
import time
import utils
from os.path import join


def list_vectorlayers(request):
  vectorlayers = VectorLayer.objects.all().order_by("upload_date");
  return render(request,"list_vectorlayers.html",{'vectorlayers':vectorlayers})

def import_shapefile(request):
    if request.method == "GET":
        form = ImportShapefileForm()
        return render(request, "import_shapefile.html",{'form':form})
    elif request.method == "POST":
        err_msg = None;
        form = ImportShapefileForm(request.POST,request.FILES)
        if form.is_valid():
          err_msg = importer.import_data(request)
        else:
          err_msg = form.errors;
        if err_msg == None:
          return HttpResponse("OK")
        else:
            return HttpResponse(err_msg);

def export_shapefile(request, vectorlayer_id):
	try:
		vectorlayer = VectorLayer.objects.get(id=vectorlayer_id)
	except VectorLayer.DoesNotExist:
		return HttpResponseNotFound()
	return exporter.export_data(vectorlayer)


def export_geojson(request, vectorlayer_id):
  try:
    vectorlayer = VectorLayer.objects.get(id=vectorlayer_id)
  except VectorLayer.DoesNotExist:
    return HttpResponseNotFound()
  geojson = exporter.export_geojson(vectorlayer)
  return JsonResponse(geojson)

def view_vectorlayer(request,vectorlayer_id):
  try:
    vectorlayer = VectorLayer.objects.get(id=vectorlayer_id)
    return render(request,"view_vectorlayer.html",{"vectorlayer":vectorlayer});
  except VectorLayer.DoesNotExist:
    return HttpResponseNotFound()  



def updateVectorLayer(vectorlayer,request):
  try:
    title = request.POST["title"]
    abstract = request.POST["abstract"]
    if(title=="" or abstract==""):
      return "Error en el formulario"

    vectorlayer.title = title;
    vectorlayer.abstract = abstract;
    vectorlayer.save()
  except Exception as e:
    return "Error " + str(e)

def edit_vectorlayer(request,vectorlayer_id):
  try:
    vectorlayer = VectorLayer.objects.get(id=vectorlayer_id)
  except VectorLayer.DoesNotExist:
    return HttpResponseNotFound()

  if request.method == "GET":
    params = {"vectorlayer":vectorlayer,"err_msg":None}
    return render(request,"update_vectorlayer.html",params)
  
  elif request.method == "POST":
    err_msg = updateVectorLayer(vectorlayer,request)
    if(err_msg==None):
      return HttpResponseRedirect("/vector")

    params = {"vectorlayer":vectorlayer,"err_msg":err_msg}
    return render(request,"update_vectorlayer.html",params)  


# Styles
def importStyle(request,vectorlayer):
  try:
    title = request.POST["title"]

    path = settings.STYLE_FILES_PATH;

    ts = time.time()
    timestamp_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
    fileName = "style_"+str(vectorlayer.id)+"_"+timestamp_str + ".sld"

    fullName = join(path,fileName)
    f = request.FILES['file']

    sld_string = f.read();
    sld_string = utils.transformSLD(sld_string);

    f.close();
    f = open(fullName,'w');
    f.write(sld_string);
    f.close();

    style = Style(file_path=path,file_name=fileName,
      title=title,vectorlayer=vectorlayer);
    style.save()
  except Exception as e:
    return "Error " + str(e)


def import_style(request,vectorlayer_id):
  try:
    vectorlayer = VectorLayer.objects.get(id=vectorlayer_id)
  except VectorLayer.DoesNotExist:
    return HttpResponseNotFound()

  if request.method == "GET":
    form = ImportStyleForm()
    return render(request,"import_style.html",{"form":form});

  if request.method == "POST":
    err_msg = None
    form = ImportStyleForm(request.POST,request.FILES)
    if form.is_valid():
      err_msg = importStyle(request,vectorlayer)
      if(err_msg==None):
        return HttpResponseRedirect("/vector")

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