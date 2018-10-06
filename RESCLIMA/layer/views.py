# -*- coding: utf-8 -*-
from django.shortcuts import render


def view_layers(request):
	return render(request,"view_layers.html")
