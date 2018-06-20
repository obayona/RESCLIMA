from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from TimeSeries.forms import *
from parsers.csv_parsers_module import *
from django.contrib import messages
from models import StationType, Station;
from django.contrib.gis.geos import Point


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

        stationType = StationType.objects.get(id=stationType_id);
        automatic = stationType.automatic;
        station = Station();
        station.serialNum = serialNum;
        station.location = Point(longitude,latitude);
        station.active = True;
        station.stationType = stationType;

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
        options = {'station_types':station_types}
        return render(request, 'new_sensor.html',options)
    elif request.method == "POST":
        err_msg = None;
        form = StationForm(request.POST)
        if form.is_valid():
            err_msg = addSensor(request.POST);
        else:
            err_msg = form.errors

        if(err_msg==None):
            return HttpResponse("OK")
        else:
            return HttpResponse(err_msg);


def upload_file(request):
    if request.method == "GET":
        form = UploadFileForm()
        return render(request, 'base_form.html', {'form': form})
    elif request.method == "POST":
        err_msg = None;
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            stationType_id = int(form.cleaned_data['stationType']);
            stationType = StationType.objects.get(id=stationType_id);
            stationType_str = str(stationType);
            file = request.FILES['file']
            if stationType_str == "HOBO-MX2300":
                err_msg = parseHOBO(file);
            elif stationType_str == "":
                err_msg = parseDataLogger(file);
            else:
                err_msg = "Error: no se reconoce ese tipo de estacion";
        else:
            err_msg = form.errors

        if(err_msg==None):
            return HttpResponse("OK")
        else:
            return HttpResponse(err_msg);