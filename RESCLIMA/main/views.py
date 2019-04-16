# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from celery.result import AsyncResult
import json
from django.core import serializers 
from dash.models import DashboardWorkspace

#METODOS DE ACCESO
def login(request):
	if (request.method == 'POST'):
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			auth_login(request, user)
			return redirect('profile')
		else:
			print("ERROR DE AUTENTICACION...")
			return render(request,'main/login.html', {'error':True})
	else:
		return render(request, 'main/login.html', {})

def logout(request):
	auth_logout(request)
	return render(request, 'main/home.html', {})

def noAccess(request):
	return render(request, 'main/noAccess.html', {})

def home(request):
	return render(request,"main/home.html")

@login_required(login_url='noAccess')
def profile(request):
	researcher = request.user.researcher
	return render(request, 'main/profile.html', {'researcher': researcher, })

#Redirecciona a la página de productos, según el rol se redireccionan a distintas páginas
def products(request):
	created_by={}
	products = DashboardWorkspace.objects.all()
	for x in products:
		created_by[x.user.username] = x.name
	return render(request, 'main/products.html', {'investigadores':created_by})


#Redirecciona a la página de ayuda y faqs
def helpfaq(request):
	researcher = request.user.researcher
	return render(request, 'main/help.html', {'researcher': researcher,})

# retorna informacion de una tarea de Celery
def get_task_info(request):
	task_id = request.GET.get('task_id', None)
	if task_id is not None:
		task = AsyncResult(task_id)
		print ("Lo que recupero  "+task_id)
		if task.result:
			if "error" in task.result:
				if task.result["error"]:
					print ("voy a imprimir un error")
					#print "el mensaje de error",task.result["error"].encode('utf-8')
		data = {}
		data["state"] = task.state
		if (task.result):
			data["result"] = task.result
		else:
			data["result"] = {}
		return HttpResponse(json.dumps(data), content_type='application/json')
	else:
		data = {}
		data["state"]="FAILURE"
		data["result"]={"error":"Error, el task se perdió"}
		return HttpResponse(json.dumps(data), content_type='application/json')

"""
Vista que sirve para guardar el archivo
de preguntas mas frecuentes para la vista
de ayuda
"""
def jsonfaqs(request):
	wrapper = FileWrapper(open('./main/static/main/json/faqs.json',"r"))
	response = HttpResponse(wrapper, content_type='application/json')
	response['Content-Disposition'] = 'attachement; filename=dump.json'
	return response

