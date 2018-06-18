from django.shortcuts import render, redirect
from TimeSeries.forms import *

def show_options(request):
  return render(request,"home_series.html")

def new_sensor(request):
    if request.method == "POST":
        form = StationForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('home_series.html')
    elif request.method == "GET":
        form = StationForm()
        return render(request, 'new_sensor.html', {'accion': 'Ingreso',
                                                'objeto': 'Sensor',
                                                'form': form,})

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['select']
            dt = 
            name = name + "_" + dt
            file = request.FILES['file']
            handle_uploaded_file(file, name)
    else:
        form = UploadFileForm()
    return render(request, 'base_form.html', {'form': form})

def handle_uploaded_file(f, name):
    with open(name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)