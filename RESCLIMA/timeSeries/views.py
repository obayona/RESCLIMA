from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from parsers.csv_parsers_module import *
from django.contrib import messages
from models import StationType, Station
from django.contrib.gis.geos import Point
from django.contrib.auth.decorators import login_required
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

def new_sensor(request):
	if request.method == "GET":
		station_types = StationType.objects.all()
		options = {'stationTypes':station_types}
		return render(request, 'new_station.html',options)
	elif request.method == "POST":
		err_msg = addSensor(request.POST);
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
		return render(request, 'timeSeries/series-visualization.html', {'measurements': json.dumps(measurements)})
	else:
		return HttpResponse("Invalid Request");

