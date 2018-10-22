from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from models import StationType, Station
from django.contrib.gis.geos import Point
from django.contrib.auth.decorators import login_required
from tasks import parseHOBOFile
from RESCLIMA import settings
from django.db import connection
import os
import time
import datetime
import json
import shutil

'''
Vista  que  retorna una  Pagina home 
de las series de tiempo, se muestran 
las opciones disponibles
'''
@login_required(login_url='noAccess')
def home(request):
	return render(request,"home_series.html")

'''
Funcion usada para ingresar una estacion.
Recibe un  diccionario con  los atributos
de  la  estacion.  Retorna None si no hay
errores,   caso   contrario   retorna  un
mensaje de error.
'''
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

'''
Vista que retorna una  Pagina que  permite
ingresar una nueva estacion. Se implementa
el metodo GET y POST.  Con GET  se retorna
la pagina y con POST se guarda la estacion
ingresada.
'''
@login_required(login_url='noAccess')
def import_station(request):
	if request.method == "GET":
		station_types = StationType.objects.all()
		options = {'stationTypes':station_types}
		return render(request, 'import_station.html',options)
	elif request.method == "POST":
		err_msg = addStation(request.POST);
		return HttpResponse(err_msg);

'''
Funcion auxiliar para guardar un archivo
Recibe un objeto UploadedFile de  django
y  guarda  el  archivo  en un directorio 
temporal. Retorna la ruta del archivo.
'''
def saveFile(ftemp):
	# directorio temporal del sistema
	temp_dir = settings.TEMPORARY_FILES_PATH;
	# se obtiene un timestamp
	t = time.time()
	ts = datetime.datetime.fromtimestamp(t)
	timestamp_str = ts.strftime('%Y-%m-%d-%H-%M-%S')
	# se genera un nuevo nombre para el archivo
	fileName = "timeseries-"+timestamp_str + ".csv"
	fullName = os.path.join(temp_dir,fileName)
	# si el objeto ftemp tiene el atributo 
	# temporary_file_path ya esta en el disco duro
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

'''
Vista que permite subir un archivo csv con
las  series de  tiempo de una  estacion no
automatica. Se implementa  el metodo GET y
POST. Con GET se  retorna la pagina, y con
POST se guardan los datos del archivo.
'''
@login_required(login_url='noAccess')
def import_file(request):
	if request.method == "GET":
		station_types = StationType.objects.filter(automatic=False)
		params = {"stationTypes":station_types}
		return render(request, 'import_file.html', params)
	elif request.method == "POST":
		stationType_id = request.POST['stationType']
		stationType = StationType.objects.get(id=stationType_id)
		stationType_str = str(stationType)
		file_ptr = request.FILES['file']
		result = {}
		# dependiendo  del  tipo  de estacion  se 
		# procede con el adptador correspondiente
		if stationType_str == "HOBO-MX2300":
			# guarda el archivo
			fileName = saveFile(file_ptr)
			params = {}
			params["fileName"]=fileName
			print "se ejecuta la tarea en celery timeserie"
			task = parseHOBOFile.delay(params)
			result["task_id"] = task.id
			print "el id del task ", task.id
			result["err_msg"] = None
		else:
			result["task_id"] = None
			result["err_msg"] = "No se reconoce este tipo de estacion"
		return HttpResponse(json.dumps(result),content_type='application/json')

def visualize(request):
	if request.method == 'GET':
#		data = {}
#		if 'variables' in request.GET:
#			variablesStr = request.GET['variables']
#			print variablesStr
#			variables = variablesStr.strip().split('|')
#			for variable in variables:
#				stationsStrStart = variable.strip().find('[')
#				stationsStrEnd = variable.strip().find(']')
#				variableId = int(variable.strip()[0:stationsStrStart])
#				stationsStr = variable.strip()[stationsStrStart+1:stationsStrEnd]
#				stationsList = stationsStr.strip().split(',')
#				stations = []
#				for stationId in stationsList:
#					stations.append(int(stationId))
#				data[variable] = stations
#		ini_date = ''
#		end_date = ''
#		if 'ini_date' in request.GET:
#			ini_date = request.GET['ini_date']
#		if 'end_date' in request.GET:
#			end_date = request.GET['end_date']
		#Call to series_searcher.py method

#	return HttpResponse("OK")
		return render(request,"view_series.html")

def get_measurements(request,variable_id, station_id, startdate, enddate):
	responseData = {'measurements': [], 'dates': [], 'variable_id': '', 'station_id': ''}
	if request.method == 'GET':
		#data = request.GET.get("info", {})
		#if len(data) > 0:
			#data = json.loads(data)
			#variableId = data.get('variable_id', '')
			#stationId = data.get('station_id', 0)
			#startDate = data.get('ini_date', '')
			#endDate = data.get('end_date', '')
		variableId = variable_id
		stationId = station_id
		startDate = startdate
		endDate = enddate
		params = []
		responseData['variable_id'] = variableId
		responseData['station_id'] = stationId
		qs = 'select readings::json->%s as measurements, ts from "timeSeries_measurement" where "idStation_id"=%s and readings like \'%%"'+variableId+'":%%\''
		params.append(variableId)
		params.append(int(stationId))
		if len(startDate) > 0 and startDate!="none":
			qs = qs + ' and ts >= %s'
			params.append(startDate)
		if len(endDate) > 0 and endDate!="none":
			qs = qs + ' and ts <= %s'
			params.append(endDate)
		qs = qs + ' order by ts;'
		with connection.cursor() as cursor:
			cursor.execute(qs, params)
			rows = cursor.fetchall()
			for row in rows:
				measurement = row[0]
				date = row[1]
				responseData['measurements'].append(measurement)
				responseData['dates'].append(date)
		qs = 'select name from \"timeSeries_variable\" where id='+variableId+';'
		cursor = connection.cursor()
		cursor.execute(qs)
		row = cursor.fetchone()
		responseData["variable_name"]=row[0]
		qs = 'select symbol from \"timeSeries_variable\" where id='+variableId+';'
		cursor = connection.cursor()
		cursor.execute(qs)
		row = cursor.fetchone()
		responseData["variable_symbol"]=row[0]
		print(row)
	return JsonResponse({"series": responseData})


