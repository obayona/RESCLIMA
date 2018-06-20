from django.shortcuts import render, redirect
from TimeSeries.forms import *
from csv_parsers_module import *
from django.contrib import messages

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
<<<<<<< HEAD
            print('holi')
            return redirect("/series")
    else:
        form = UploadFileForm()
    return render(request, 'base_form.html', {'form': form})
=======
            station_type = form.cleaned_data['select']
            file = request.FILES['file']
            if(station_type = "HOBO-MX2300"):
                try:
                    result = parseHOBO(file)
                    messages.success(request, 'Successfully saved')
                except KeyError:
                    messages.error(request, 'Could not save the file.', extra_tags='alert')
                    
    else:
        form = UploadFileForm()
    return render(request, 'base_form.html', {'form': form})

>>>>>>> remotes/origin/upload-files
