# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from celery.result import AsyncResult
import json

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
"""
def logout(request):
	auth_logout(request)
	return render(request, 'main/home.html', {})"""

def noAccess(request):
	return render(request, 'main/noAccess.html', {})

def home(request):
    	return render(request,"main/home.html")

@login_required(login_url='noAccess')
def profile(request):
	researcher = request.user.researcher
	return render(request, 'main/profile.html', {'researcher': researcher, })


# retorna informacion de una tarea de Celery
def get_task_info(request):
	task_id = request.GET.get('task_id', None)
	if task_id is not None:
		task = AsyncResult(task_id)
		print "Lo que recupero  ",task.state
		if task.result:
			if "error" in task.result:
				if task.result["error"]:
					print "voy a imprimir un error"
					print "el mensaje de error",task.result["error"].encode('utf-8')
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


