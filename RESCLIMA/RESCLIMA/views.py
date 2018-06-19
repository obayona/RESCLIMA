from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from models import Researcher

#METODOS DE ACCESO
def login(request):
    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            print("ERROR DE AUTENTICACION...")
            return render(request,'login.html', {'error':True})
    else:
        return render(request, 'login.html', {})

def logout(request):
    auth_logout(request)
    return render(request, 'home.html', {})

def noAccess(request):
    return render(request, 'noAccess.html', {})

def home(request):
  return render(request,"home.html")

@login_required()
def dashboard(request):
    researcher = request.user.researcher
    return render(request, 'dashboard.html', {'researcher': researcher, })