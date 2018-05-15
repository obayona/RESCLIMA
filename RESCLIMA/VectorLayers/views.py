from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotFound, JsonResponse
from django.http import HttpResponseRedirect
from models import VectorLayer
from forms import ImportShapefileForm
import importer, exporter
from django.views.generic.edit import UpdateView

def list_vectorlayers(request):
  vectorlayers = VectorLayer.objects.all().order_by("filename");
  return render(request,"list_vectorlayers.html",{'vectorlayers':vectorlayers})

def import_shapefile(request):
    if request.method == "GET":
        form = ImportShapefileForm()
        return render(request, "import_shapefile.html",{'form':form})
    elif request.method == "POST":
        form = ImportShapefileForm(request.POST,request.FILES)
        
        if form.is_valid():
            err_msg = importer.import_data(request)
            if err_msg == None:
                return HttpResponse("OK")
        else:
            err_msg = "Error en el formulario"
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
  return render(request,"view_vectorlayer.html",{"vectorlayer_id":vectorlayer_id});  

class VectorLayerUpdate(UpdateView):
    model = VectorLayer
    fields = ['title','abstract']
    template_name_suffix = '_update_form'
    success_url = '/vector/'
