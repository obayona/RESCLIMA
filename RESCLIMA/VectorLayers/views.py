from django.shortcuts import render
from django.http import HttpResponse
from models import VectorFile
from django.http import HttpResponseRedirect
from forms import ImportShapefileForm
import importer, exporter
from django.http import HttpResponseNotFound, JsonResponse

def import_shapefile(request):
    if request.method == "GET":
        form = ImportShapefileForm()
        return render(request, "import_shapefiles.html",
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
        return render(request, "import_shapefiles.html",
                      {'form'    : form,
                       'err_msg' : err_msg})

def export_shapefile(request, shapefile_id):
	try:
		vectorfile = VectorFile.objects.get(id=shapefile_id)
	except VectorFile.DoesNotExist:
		return HttpResponseNotFound()
	return exporter.export_data(vectorfile)

def list_vectorfiles(request):
  vectorfiles = VectorFile.objects.all().order_by("filename");
  return render(request,"list_vectorfiles.html",{'vectorfiles':vectorfiles})

def export_geojson(request, vectorfile_id):
  try:
    vectorfile = VectorFile.objects.get(id=vectorfile_id)
  except VectorFile.DoesNotExist:
    return HttpResponseNotFound()
  geojson = exporter.export_geojson(vectorfile)
  return JsonResponse(geojson)


