# -*- encoding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from datetime import datetime
from dateutil.parser import parse
from timeSeries.models import Variable,Station,Measurement
from timeSeries.utils import *
import os
from celery import shared_task, current_task

# parseHobo(file)
# Recibe un objeto de tipo UploadedFile
# (clase de django). Obtiene los datos del archivo csv
# y los guarda en la base de datos.
# El archivo csv, contiene las mediciones a lo largo
# del tiempo de varias variables que fueron medidas con una
# estacion meteorologica de tipo HOBO-MX2300.
# Del archivo se puede recuperar: la estacion meteorologica,
# las variables y las mediciones con su datetime
@shared_task
def parseHOBOFile(hoboParams):
	# se obtiene el nombre del archivo
	fileName = hoboParams["fileName"]
	print "empieza el task hobo"
	'''
	Diccionario con el resultado de la operacion.
	Este  diccionario  estara dentro de un objeto 
	celery.result.AsyncResult
	result = {
				"error": string  con  mensaje de error, 
						 si no hay error, esta clave no 
						 existira o sera None
				"percent": porcentaje de progreso de la
						   operacion
			}
	'''
	result = {}
	# abre el archivo
	f = None
	if os.path.isfile(fileName):
		f = open(fileName,'r')
	else:
		result["error"]="Error, se perdio el archivo"+fileName;
		current_task.update_state(state='FAILURE',meta=result)
		return result

	'''
	se comprueba  el numero de  lineas del 
	archivo se requieren al menos 3 lineas
	1era linea: contiene el numero de serie de la estacion
	2da linea: contiene el header del csv
	3ra linea: datos
	'''
	print "voy a contar las lineas"
	num_lines = count_file_lines(f)
	if (num_lines<3):
		result["error"]="Error: archivo sin datos";
		current_task.update_state(state='FAILURE',meta=result)
		return result

	print "numero de lineas",num_lines
	# formato de la fecha
	datetime_format = "%m/%d/%y %I:%M:%S %p";
	# time zone de las fechas de los datos (ej.: UTC,GMT+2,GMT-4,etc)
	local_tz_str = None;
	# numero de serie de la estacion
	serialNum = None;
	# objeto con datos de la estacion
	station = None;
	# las variables del archivo
	variables = []

	# actualiza el porcentaje de avance de la tarea: 5%
	result["error"]=None
	result["percent"]=5
	current_task.update_state(state='PROGRESS',meta=result)


	percent_cont = 0
	# se itera el archivo
	for i,line in enumerate(f,1):
		#line = line.encode('utf-8')
		# si se lee la primera linea del archivo
		# se recupera el numero serial de la estacion
		print i
		if(i==1):
			print "linea 1"
			# la primera linea contiene "string1: string2"
			# string2 es el  numero serial  de la estacion
			parts = line.split(":")
			if (len(parts)==2):
				serialNum = parts[1]
				serialNum = serialNum.strip(' \t\n\r')
			else:
				# se borra el archivo
				os.remove(fileName)
				result["error"]="Error: no se especifica el numero de serie de la estacion"
				current_task.update_state(state='FAILURE',meta=result)
				return result

			# se valida que la estacion existe en la base de datos
			results=Station.objects.filter(serialNum=serialNum);
			if(results.count()!=1):
				# se borra el archivo
				os.remove(fileName)
				result["error"]="Error: no se encontro la estacion "+serialNum
				current_task.update_state(state='FAILURE',meta=result)
				return result
			else:
				station = results[0]

			# se comprueba que el tipo de stacion sea HOBO-MX2300
			typestation = str(station.stationType)
			if(typestation!="HOBO-MX2300"):
				# se borra el archivo
				os.remove(fileName)
				result["error"]="Error: la estacion debe ser de tipo HOBO-MX2300"
				current_task.update_state(state='FAILURE',meta=result)
				return result


			result["percent"]=10
			current_task.update_state(state='PROGRESS',meta=result)

			continue;

		# si se lee la segunda linea
		# se tienen los headers
		if(i==2):
			print "linea 2"
			headers = line.split("\t");
			if len(headers)!=8:
				# se borra el archivo
				os.remove(fileName)
				msg = "Error: el archivo debe tener ocho columnas, "
				ms = msg + "se tienen "+str(len(headers)) + " columnas"
				result["error"]=msg
				current_task.update_state(state='FAILURE',meta=result)
				return result

			# se obtiene la informacion del timezone
			# el string debe ser parseado para obtener el ofset 
			# en horas
			header_date = headers[1]
			index = header_date.find("GMT")
			time_zone_str = header_date[index:].strip(' \t\n\r')
			ofset_str = time_zone_str[3:]
			index = ofset_str.find(":")
			ofset_str = ofset_str[:index]
			ofset = int(ofset_str)
			# se crea el string del timezone
			if(ofset<0):
				local_tz_str = "Etc/GMT-" + str(abs(ofset));
			elif(ofset >0):
				local_tz_str = "Etc/GMT+" + str(abs(ofset));
			else:
				local_tz_str="UTC";


			# La primera columna es un contador
			# y la segunda columna es la fecha.
			# Se las ignora
			headers = headers[2:];

			# se crea un diccionario con los nombres
			# de las variables
			name_dict = {}
			name_dict[0] = u"Temperatura"
			name_dict[1] = u"Humedad relativa"
			name_dict[2] = u"Lluvia"
			name_dict[3] = u"Dirección del viento"
			name_dict[4] = u"Velocidad del viento"
			name_dict[5] = u"Velocidad de rafagas"

			# se recuperan los pk de las variables
			for index,header in enumerate(headers):
				# se busca la variable por el nombre
				results = Variable.objects.filter(name=name_dict[index]);
				if(results.count()!=1):
					# se borra el archivo
					os.remove(fileName)
					result["error"]="Error: No existe la variable "+name_dict[index]
					current_task.update_state(state='FAILURE',meta=result)
					return result

				variable = results[0];
				# se guarda en la lista el id de la
				# variable
				variables.append(variable);

			# se actualiza el progreso
			result["percent"]=20
			current_task.update_state(state='PROGRESS',meta=result)

			continue;

		print "linea",i
		# si la linea es mayor que la 2
		# se obtienen las mediciones
		measures = line.split("\t")
		if(len(measures)!=8):
			# se borra el archivo
			os.remove(fileName)
			result["error"]="Error: falta una columna en la linea "+str(i)
			current_task.update_state(state='FAILURE',meta=result)
			return result
		# se recupera la fecha hora de la segunda columna
		datetime_str = measures[1]
		try:
			# se crea un objeto datetime desde el string y el formato
			dt = datetime.strptime(datetime_str,datetime_format);
			# se transforma la fecha del time zone local a UTC
			dt = transformToUTC(dt,local_tz_str);
		except Exception as e:
			# se borra el archivo
			os.remove(fileName)
			result["error"]="Error: la fecha "+datetime_str+" no es correcta"+str(e)
			current_task.update_state(state='FAILURE',meta=result)
			return result

		# se obtienen las mediciones
		# se remueven las dos primeras columnas
		measures = measures[2:]
		measures_dict = {}
		for index,measure in enumerate(measures):
			if measure == "":
				continue;

			variable = variables[index]
			idVariable = variable.id;
			datatype = variable.datatype;
			measure = parseMeasure(measure,datatype);
			# se agrega al diccionario de variables y
			# mediciones
			measures_dict[idVariable]=measure;
		
		# se guardan las mediciones
		saveMeasurements(station,None,measures_dict, dt);

		# se actualiza el porcentaje de progreso de 30 a 90
		percent_cont = percent_cont%10
		percent_cont += 1
		# cada 50 lineas actualiza el progreso
		if(percent_cont==0):
			percent = 30 + (float(i)/num_lines)*75
			result["error"]=None
			result["percent"]=percent
			current_task.update_state(state='PROGRESS',meta=result)
		

	# se completa la tarea
	result["percent"]=100		
	return result

