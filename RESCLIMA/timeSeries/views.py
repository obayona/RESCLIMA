from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from models import StationType, Station
from django.contrib.gis.geos import Point
from django.contrib.auth.decorators import login_required
from django.db import connection
import json

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

def import_station(request):
	if request.method == "GET":
		station_types = StationType.objects.all()
		options = {'stationTypes':station_types}
		return render(request, 'new_station.html',options)
	elif request.method == "POST":
		err_msg = addStation(request.POST);
		return HttpResponse(err_msg);


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
	responseData = {'measurements': {}, 'variable_id': ''}
	if request.method == 'POST' and request.is_ajax:
		data = request.POST["info"]
		data = json.loads(data)
		variableId = data['variable_id']
		starionsList = data['stations_list']
		startDate = data['ini_date']
		endDate = data['end_date']
		params = []
		responseData['variable_id'] = variableId
		for stationId in starionsList:
			qs = 'select "timeSeries_measurement"."idStation_id" as id_station, readings::json->%s as measurements, ts from "timeSeries_measurement" where "idStation_id"=%s and readings like "%%%s:%"'
			params.append(variableId)
			params.append(stationId)
			params.append(variableId)
			if len(startDate) > 0:
				qs = qs + ' and ts >= %s'
				params.append(startDate)
			if len(endDate) > 0:
				qs = qs + ' and ts <= %s'
				params.append(endDate)
			qs = qs + ' order by ts;'
		print("====================")
		print(params)
		print(qs)
		with connection.cursor() as cursor:
			cursor.execute(qs, ['6', '1','6', '2018-10-09', '2018-10-12'])
			rows = cursor.fetchall()
			for row in rows:
				idStation = row[0]
				measurement = row[1]
				date = row[2]
				if idStation not in responseData['measurements']:
					responseData['measurements'][idStation] = {}
				if date not in responseData['measurements'][idStation]:
					responseData['measurements'][idStation][date] = []
				responseData['measurements'][idStation][date].append(measurement)

	return JsonResponse({"series": responseData})
