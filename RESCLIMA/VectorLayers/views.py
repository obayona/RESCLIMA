from django.shortcuts import render
from django.http import HttpResponse
from models import VectorLayer
from django.http import HttpResponseRedirect
from forms import ImportShapefileForm
import importer, exporter
from django.http import HttpResponseNotFound, JsonResponse


def list_vectorlayers(request):
  vectorlayers = VectorLayer.objects.all().order_by("filename");
  return render(request,"list_vectorlayers.html",{'vectorlayers':vectorlayers})

def import_shapefile(request):
    if request.method == "GET":
        form = ImportShapefileForm()
        return render(request, "import_shapefile.html",
                      {'form'    : form,
                       'err_msg' : None})
    elif request.method == "POST":
        form = ImportShapefileForm(request.POST,
                                   request.FILES)
        if form.is_valid():
            shapefile = request.FILES['import_file']
            encoding  = request.POST['character_encoding']
            err_msg = importer.import_data(shapefile,
                                                encoding)
            if err_msg == None:
                return HttpResponseRedirect("/vector")
        else:
            err_msg = None
        return render(request, "import_shapefile.html",
                      {'form'    : form,
                       'err_msg' : err_msg})

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
  return render(request,"view_vectorlayer.html",{"vectorlayer_id":vectorlayer_id});  
