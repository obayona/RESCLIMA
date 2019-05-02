from django.shortcuts import render
from django.conf import settings
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from django.views.generic.edit import FormView
from django.views.generic import *

from sensor.models import *
from sensor.forms import *

# Create your views here.
class SensoresCreate(CreateView):
	template_name = 'sensor/form.html'
	form_class = SensorForm
	success_url = reverse_lazy('sensor_list')

	def form_valid(self, form):
		sensor_instance = form.save(commit=False)
		sensor_instance.user = self.request.user
		sensor_instance.save()
	
		return super(SensoresCreate,self).form_valid(form)

class SensoresList(TemplateView):
	template_name = 'sensor/list.html'

	def get_data(self, **kwargs):
		context = super(SensoresList, self).get_data(**kwargs)
		try:
			context['object_list'] = Sensor.objects.filter(order_by('date'))
			print(context['object_list'])
		except Sensor.DoesNotExist:
			context['object_list'] = None
		return context


limit = 10
@login_required(login_url='noAccess')
def list_sensors(request):
	researcher = request.user.researcher
	researcher = researcher.id
	sensors = Sensor.objects.all()
	page = request.GET.get('page',1)
	paginator = Paginator(sensors, limit)
	try:
		sensores = paginator.page(page)
	except PageNotAnInteger:
		sensores = paginator.page(1)
	except EmptyPage:
		sensores = paginator.page(paginator.num_pages)
	return render(request, "sensor/list.html", {'object_list':sensores})


class SensoresUpdate(UpdateView):
	model = Sensor
	form_class = SensorForm
	template_name = 'sensor/form.html'
	success_url = reverse_lazy('sensor_list')

	def form_valid(self, form):
		sensor_instance = form.save(commit=False)
		sensor_instance.user = self.request.user
		sensor_instance.save()

		return super(SensoresUpdate,self).form_valid(form)

class SensorDelete(DeleteView):
	model = Sensor
	template_name = 'sensor/delete.html'
	success_url = reverse_lazy('sensor_list')
