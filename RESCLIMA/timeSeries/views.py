from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from models import StationType, Station
from django.contrib.gis.geos import Point
from django.contrib.auth.decorators import login_required
from django.db import connection
import json
from django.http import JsonResponse

@login_required(login_url='noAccess')
def show_options(request):
	return render(request,"home_series.html")


def addSensor(data):
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

@login_required(login_url='noAccess')
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
@login_required(login_url='noAccess')
def upload_file(request):
	if request.method == "GET":
		station_types = StationType.objects.filter(automatic=False)
		params = {"stationTypes":station_types}
		return render(request, 'import_file.html', params)
	elif request.method == "POST":
		err_msg = None;
		stationType_id = request.POST['stationType'];
		stationType = StationType.objects.get(id=stationType_id);
		stationType_str = str(stationType);
		file_ptr = request.FILES['file']
		if stationType_str == "HOBO-MX2300":
			err_msg = parseHOBO(file_ptr);
		elif stationType_str == "":
			err_msg = parseDataLogger(file_ptr);
		else:
			err_msg = "Error: no se reconoce ese tipo de estacion";

		if(err_msg=="Success"):
			return HttpResponse("OK")
		else:
			return HttpResponse(err_msg);


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
		return render(request,"series-visualization.html")

def get_measurements(request):
	responseData = {'measurements': [], 'dates': [], 'variable_id': '', 'station_id': ''}
	if request.method == 'POST' and request.is_ajax:
		data = request.POST.get("info", {})
		if len(data) > 0:
			data = json.loads(data)
			variableId = data.get('variable_id', '')
			stationId = data.get('station_id', 0)
			startDate = data.get('ini_date', '')
			endDate = data.get('end_date', '')
			params = []
			responseData['variable_id'] = variableId
			responseData['station_id'] = stationId
			qs = 'select readings::json->%s as measurements, ts from "timeSeries_measurement" where "idStation_id"=%s and readings like \'%%"'+variableId+'":%%\''
			params.append(variableId)
			params.append(int(stationId))
			if len(startDate) > 0:
				qs = qs + ' and ts >= %s'
				params.append(startDate)
			if len(endDate) > 0:
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
	return JsonResponse({"series": responseData})
