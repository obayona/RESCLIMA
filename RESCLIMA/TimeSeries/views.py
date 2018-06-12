from django.shortcuts import render, redirect
from TimeSeries.forms import *

def show_options(request):
  return render(request,"home.html")

def new_sensor(request):
    if request.method == "POST":
        form = StationForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('home')
    elif request.method == "GET":
        form = StationForm()
        return render(request, 'newSensor.html', {'accion': 'Ingreso',
                                                'objeto': 'Sensor',
                                                'form': form,})

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print('holi')
    else:
        form = UploadFileForm()
    return render(request, 'baseform.html', {'form': form})