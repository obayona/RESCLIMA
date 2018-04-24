from django.shortcuts import render

def newSensor(request):
    if request.method == "POST":
        form = SensorForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('home')
    elif request.method == "GET":
        form = SensorForm()
        return render(request, 'baseform.html', {'accion': 'Ingreso',
                                                'objeto': 'Sensor',
                                                'form': form,})
