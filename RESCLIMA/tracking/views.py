# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import default_storage

from django.views.generic.edit import FormView
from django.views.generic import *

from tracking.models import *
from tracking.forms import *
from tracking.utils import *
from tracking.tasks import *
from tracking.exporter import *

from django.conf import settings
from django.urls import reverse_lazy

import json
from geojson import Polygon
import traceback
import xml.etree.ElementTree as ET

import RESCLIMA.settings as settings
from layer.utils import getLayerBBox

def view_tracks(request):
	sensores = Sensor.objects.all()
	content = {}

	for sense in sensores:
		content[sense.id] = sense.name

	return render(request,"view_tracks.html", {"sensores":content})


class TrackFileCreate(CreateView):
	template_name = 'tracking/form.html'
	form_class 	  = TrackFileForm
	success_url = reverse_lazy('trackfile_list') 

	def form_valid(self, form):
		file_instance =form.save(commit=False)
		file_instance.user = self.request.user
		file_instance.sensor = Sensor.objects.all().filter(id=form.fields['sensor'])
		file_instance.save()

		for f in self.request.FILES.getlist('file'):
			try:
				file_instance = TracksFile(tracking=file_instance, file=f)
				file_name = default_storage.save(f.name, f)
				file_instance.save()
			except Exception as e:
				traceback.print_exc()

		return super(TrackFileCreate, self).form_valid(form)

class TrackFileList(TemplateView):
	template_name = 'tracking/list.html'
	
	def get_context_data(self,**kwargs):
		context = super(TrackFileList,self).get_context_data(**kwargs)
		try:
			context['object_list'] = TracksFile.objects.all()
		except TracksFile.DoesNotExist:
			context['object_list'] = None
		return context

class TrackFileUpdate(UpdateView):
	model = TracksFile
	form_class = TrackFileForm
	template_name = 'tracking/form.html'
	success_url = reverse_lazy('trackfile_list')

	def form_valid(self, form):
		track_instance =form.save(commit=False)
		track_instance.user = self.request.user
		print(form.fields['sensor'])
		file_instance.sensor = Sensor.objects.all().filter(id=form.fields['sensor'])
		track_instance.save()

		for f in self.request.FILES.getlist('file'):
			try:
				file_instance = TracksFile(tracking=track_instance, file=f)
				file_name = default_storage.save(f.name, f)
				file_instance.save()
			except:
				traceback.print_exc()

		return super(TrackFileUpdate, self).form_valid(form)


class TrackFileDelete(DeleteView):
	model = TracksFile
	template_name = 'tracking/delete.html'
	success_url = reverse_lazy('trackfile_list')

# Busca los datos segun la fecha en que se quiere revisar los datos del
# track del sensor, crea un asrchivo gpx con los valores relevantes y 
# retorna sus datos como un HttpResponse para facilitar ser agregado
# en una layer dinamica usando la libreria de OSMap
def track_files_generator(request, id_sensor, date_init, date_end):
	date_format = "%Y-%m-%dT%H:%M:%SZ" 
	date_init = datetime.strptime(date_init, date_format)
	date_end  = datetime.strptime(date_end, date_format)

	track_sensor = TrackPoint.objects.filter(sensor_id=id_sensor, date_start__gt=date_init,date_end__lt=date_end)

	track_json = {}

	track_json['sensor'] = id_sensor
	track_json['lonlat'] = track_sensor.measured_points

	meta_data = {}
	meta_data["name"] = id_sensor
	meta_data["lat"]  = track_sensor.measured_points[0]["lat"]
	meta_data["lon"]  = track_sensor.measured_points[0]["lon"]
	meta_data["ele"]  = track_sensor.measured_points[0]["ele"]

	##genera un string de un archivo .gpx con los valores de lon lat y ele
	gpx_str = generateGPx(track_json['lonlat'], meta_data)

	file_name = "trackfile_"+id_sensor+"_"+str(date_init)+"_"+str(date_end)
	try:
		gpx_path = save_traffic_data_file(gpx_str,file_name)
		full_path = settings.TEMPORARY_FILES_PATH
		fullName = os.path.join(full_path, file_name)
		
		f = open(fullName,'r')
		gpx = f.read()
		return HttpResponse(gpx)
	
	except Exception as e:
		return HttpResponseNotFound()


def get_info_sensor(request, id_sensor):
	try:
		sensor = Sensor.objects.get(id=id_sensor)
		layer_json = {}
		layer_json["id"]=id_sensor
		layer_json['name']= sensor.name
		layer_json["description"]=sensor.description
		data_date_str = str(sensor.date)
		data_date_str = data_date_str.replace("-","/")
		layer_json["data_date"]=data_date_str

		return HttpResponse(json.dumps(layer_json),content_type='application/json')

	except Exception as e:
		return HttpResponseNotFound()


'''
Function that shows tracking data from gpx files, according
a sensor, initial and final date
'''
def track_files_viewer(request, id_sensor, date_init, date_end):

	path = "sensor"+id_sensor+"-"+date_init+"-"+date_end+".gpx"
	path = "/"+os.path.join(settings.GPX_FILES_PATH, path)
	#path = '/home/manuel/manager/gpx/sensor3-2018-06-02-2018-06-03.gpx'
	try:
		wrapper = FileWrapper(open(path,"rb"))
		response = HttpResponse(wrapper, content_type='application/gpx')
		response['Content-Disposition'] = 'attachement; filename=dump.gpx'
		return response
	except Exception as e:
		print(e)
		return HttpResponseNotFound()

'''
Function that parses a .gpx file to get the original lat and lon
values to set the center of the map
'''
def getmetadata_gpx(request, id_sensor, date_init, date_end):
	path = "sensor"+id_sensor+"-"+date_init+"-"+date_end+".gpx"
	path = "/"+os.path.join(settings.GPX_FILES_PATH, path)

	tree = ET.parse(path)
	metadata_json = {}
	namespace = {"gpx": "http://www.topografix.com/GPX/1/0"}
	'bounds minlat="45.735199945" minlon="14.288633270" maxlat="45.795349991" maxlon="14.377516648"'
	try: 
		for elem in tree.findall('gpx:bounds', namespace):
			value_mid = ((float(elem.attrib['minlat']) + float(elem.attrib['minlat']))/2) , ((float(elem.attrib['maxlon'])+ float(elem.attrib['minlon']))/2)
			metadata_json["bbox"]= Polygon([[( float(elem.attrib['minlat']),
												float(elem.attrib['minlon']) ),
											( value_mid),
											 ( float(elem.attrib['maxlat']),
												float(elem.attrib['maxlon']) )]])

		for elem in tree.findall('gpx:wpt', namespace):
			metadata_json["lon"] = elem.attrib['lon']
			metadata_json["lat"] = elem.attrib['lat']
			if 'ele' in elem.attrib:
				metadata_json["ele"] = elem.attrib['ele']
			print(metadata_json)
			return HttpResponse(json.dumps(metadata_json),content_type='application/json')

	except Exception as e:
		return HttpResponseNotFound()