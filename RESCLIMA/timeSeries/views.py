from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from models import StationType, Station
from django.contrib.gis.geos import Point
from django.contrib.auth.decorators import login_required
from tasks import parseHOBOFile
from RESCLIMA import settings
import os
import time
import datetime
import json
import shutil

# es la pagina principal de la app
@login_required(login_url='noAccess')
def show_options(request):
	return render(request,"home_series.html")

# funcion para agregar una estacion
def addStation(data):
	try:
		stationType_id = int(data["stationType"]);
		serialNum = data["serialNum"];
		latitude = float(data["latitude"]);
		longitude = float(data["longitude"]);
		frequency = data["frequency"];
		token = data["token"];

		# se recupera el tipo de estacion
		stationType = StationType.objects.get(id=stationType_id);
		automatic = stationType.automatic;
		# se crea una estacion
		station = Station();
		station.serialNum = serialNum;
		station.location = Point(longitude,latitude);
		station.active = True;
		station.stationType = stationType;

		# si la estacion es automatica
		# se agregan la frecuencia
		# y el token
		if(automatic==True):
			if(frequency == "" or token == ""):
				return "Error: faltan argumentos";
			frequency = float(frequency);
			if(frequency<=0):
				return "Error: frecuencia debe ser mayor que cero"
			station.frequency = frequency;
			station.token = token;

		station.save();
	except Exception as e:
		return "Error " + str(e)

	return None

# view para agregar una estacion
def import_station(request):
	if request.method == "GET":
		station_types = StationType.objects.all()
		options = {'stationTypes':station_types}
		return render(request, 'new_station.html',options)
	elif request.method == "POST":
		err_msg = addStation(request.POST);
		return HttpResponse(err_msg);


# funcion auxiliar para guardar un archivo
def saveFile(ftemp):

	temp_dir = settings.TEMPORARY_FILES_PATH;
	# se obtiene un timestamp
	ts = time.time()
	timestamp_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
	# se genera un nuevo nombre para el archivo
	fileName = "timeseries-"+timestamp_str + ".csv"
	fullName = os.path.join(temp_dir,fileName)
	# si el objeto tiene el atributo temporary_file_path
	# ya esta en el disco duro
	if (hasattr(ftemp,'temporary_file_path')):
		ftemp_path = ftemp.temporary_file_path()
		# mueve el archivo
		shutil.move(ftemp_path,fullName)
	else:
		# el archivo esta en memoria y se debe 
		# escribir en el disco
		f = open(fullName,'w')
		for chunk in ftemp.chunks():
			f.write(chunk)
		f.close()

	return fullName


# view que permite subir un archivo csv
def upload_file(request):
	if request.method == "GET":
		station_types = StationType.objects.filter(automatic=False)
		params = {"stationTypes":station_types}
		return render(request, 'import_file.html', params)
	elif request.method == "POST":
		stationType_id = request.POST['stationType']
		stationType = StationType.objects.get(id=stationType_id)
		stationType_str = str(stationType)
		file_ptr = request.FILES['file']

		# guarda el archivo
		fileName = saveFile(file_ptr)
		params = {}
		params["fileName"]=fileName
		print params, "los parametros ***"
		result = {}
		# dependiendo  del  tipo  de estacion  se 
		# procede con el adptador correspondiente
		if stationType_str == "HOBO-MX2300":
			print "se ejecuta la tarea en celery timeserie"
			task = parseHOBOFile.delay(params)
			result["task_id"] = task.id
			print "el id del task ", task.id
			result["err_msg"] = None
		else:
			result["task_id"] = None
			result["err_msg"] = "No se reconoce este tipo de estacion"
		# se borra el archivo temporal
		#os.remove(fileName)
		# se retorna el resultado
		return HttpResponse(json.dumps(result),content_type='application/json')


def visualize(request):
	if request.method == 'GET':
		if 'variables' in request.GET:
			variablesStr = request.GET['variables']
			print variablesStr
			variables = variablesStr.strip().split('|')
			for variable in variables:
				stationsStrStart = variable.strip().find('[')
				stationsStrEnd = variable.strip().find(']')
				variableId = int(variable.strip()[0:stationsStrStart])
				stationsStr = variable.strip()[stationsStrStart+1:stationsStrEnd]
				stationsList = stationsStr.strip().split(',')
				stations = []
				for stationId in stationsList:
					stations.append(int(stationId))
		ini_date = ''
		end_date = ''
		if 'ini_date' in request.GET:
			ini_date = request.GET['ini_date']
		if 'end_date' in request.GET:
			end_date = request.GET['end_date']
		#Call to series_searcher.py method
		measurements={}
		return render(request, 'series-visualization.html', {'measurements': json.dumps(measurements)})
	else:
		return HttpResponse("Invalid Request");
