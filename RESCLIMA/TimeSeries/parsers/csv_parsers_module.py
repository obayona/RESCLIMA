import configparser
from datetime import datetime
import pytz
from dateutil.parser import parse
from TimeSeries.models import *
import os

__ERROR_MESSAGES__ = {
	"uknown_station": "uknown station - not in config file", 
	"no_station_id": "No id in HOBO-MX2300 file",
	"invalid_len": "File is too small",
	"user_message": "Error al procesar su archivo",
	"no_columns": "Not enough columns"
}

def parseHOBO(file):
	"""Parse HOBO file"""
	global __ERROR_MESSAGES__
	STATION="HOBO"
	#check file length
	if is_valid_len(file,4) == False:
		print (__ERROR_MESSAGES__["invalid_len"])
		return (__ERROR_MESSAGES__["user_message"])

	module_dir = os.path.dirname(__file__)
	config_file_path = os.path.join(module_dir, 'meteo_stations.cfg')
	config = configparser.ConfigParser()
	config.read(config_file_path)
	#check for file 
	if "HOBO" not in config.sections():
		print (__ERROR_MESSAGES__["unknown_station"])
		return __ERROR_MESSAGES__["user_message"]

	headers = int (config.get(STATION,"headers"))
	datetime_format = str(config.get(STATION,"datetime_format"))
	date_pos = int(config.get(STATION,"date_pos")) - 1

	datetime_format = "%m/%d/%y %I:%M:%S %p";
	local_tz_str = None;
	serialNum = None;
	station = None;
	variables = []
	blanks = 0

	# se itera el archivo
	for i, line in enumerate(file,1):
		# si se lee la primera linea del archivo
		# se recupera el numero serial de la estacion
		if(i==1):
			# la primera linea contiene
			# string: string
			# El segundo string es el serial de la estacion
			parts = line.split(":")
			if (len(parts)==2):
				serialNum = parts[1]
				serialNum = serialNum.strip(' \t\n\r')
			else:
				return __ERROR_MESSAGES__["no_station_id"]

			# se valida que la estacion existe en la base de datos
			results=Station.objects.filter(serialNum=serialNum);
			if(results.count()!=1):
				return __ERROR_MESSAGES__["uknown_station"]
			else:
				station = results[0]

			# se comprueba que el tipo de stacion sea HOBO-
			typestation = str(station.stationType)
			if(typestation!="HOBO-MX2300"):
				return "Error: la estacion debe ser de tipo HOBO-MX2300"

			continue;
		# si se lee la segunda linea del archivo
		# se tienen los headers
		if(i==2):
			headers = line.split("\t");
			if len(headers)!=8:
				msg = "Error: el archivo debe tener ocho columnas, "
				ms = msg + "se tienen "+str(len(headers)) + " columnas"
				return msg

			# se obtiene la informacion del timezone
			# el string debe ser parseado para obtener el ofset en
			# horas
			header_date = headers[1]
			index = header_date.find("GMT")
			time_zone_str = header_date[index:].strip(' \t\n\r')
			ofset_str = time_zone_str[3:]
			index = ofset_str.find(":")
			ofset_str = ofset_str[:index]
			ofset = int(ofset_str)

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
			# se recuperan los pk de las variables
			for alias in headers:
				# se busca por el alias
				# a la variable
				alias = alias.strip(' \t\n\r');
				results = Variable.objects.filter(alias=alias);
				if(results.count()!=1):
					return "Error: No existe la variable " + alias
				variable = results[0];
				# se guarda en la lista el id de la
				# variable
				variables.append(variable);

			continue;

		# si la linea es mayor que la 2
		# se obtienen las mediciones
		measures = line.split("\t")
		if(len(measures)!=8):
			return "Error: falta una columna en: "+line
		# se recupera la fecha hora de la segunda columna
		datetime_str = measures[1]
		try:
			# se crea un objeto datetime del string y del formato
			dt = datetime.strptime(datetime_str,datetime_format);
			# se transforma la fecha del time zone local a UTC
			dt = transformToUTC(dt,local_tz_str);
		except Exception as e:
			return "Error: la fecha "+datetime_str+" no es correcta "+str(e)



		# se remueven las dos primeras columnas
		measures = measures[2:]
		measures_dict = {}
		for index,measure in enumerate(measures):
			if measure == "":
				blanks = blanks + 1
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
		
	return "Success",blanks
		

def parseCF200(file):
	"""Parse Datalogger CF200 file"""
	STATION = "CF200"
	config = configparser.ConfigParser()
	config.read("meteo_stations.cfg")
	if "CF200" not in config.sections():
		print "Meteorological station not configured. Exit..."
		sys.exit()
	file = open(file,"r")
	headers= int (config.get(STATION,"headers"))
	#read verbose headers
	for i in range(headers):
		file.readline()
	#start reading the file
	for line in file:
		print line
		measures = line.strip().split(",")
		#Parse timestamp as it can be a datetime or date and time independent fields
		date_pos = int(config.get(STATION,"date_pos"))-1
		time_pos = date_pos + 1
		date = measures[date_pos]
		time = measures[time_pos]
		ts = parseDatetime(date,time)
		fields = config.get(STATION,"fields")
		fields = fields.strip().split(",")
		print "\n"

	return None

def parseDatetime(date, time = None):
	if time != None:
		date = date.strip()
		time = time.strip()
		ts = parse(date+" "+time)
	else:
		ts = parse(date)
	return ts

def transformToUTC(dt,local_tz_str):
	if(local_tz_str=="UTC"):
		return dt
	local_tz = pytz.timezone (local_tz_str);
	dt_with_tz = local_tz.localize(dt, is_dst=None)
	dt_in_utc = dt_with_tz.astimezone(pytz.utc)
	return dt_in_utc;




# pendiente validad boolean
def parseMeasure(measure,datatype):
	if(datatype=="float"):
		return float(measure);
	if(datatype=="string"):
		return measure;
	if(datatype=="boolean"):
		return True;


def saveMeasurements(station,id_provider,measurements_dict,datetime = datetime.now()):

	if id_provider == None and station!= None:
		measurement = Measurement(idStation = station, datetime = datetime, readings = measurements_dict, idProvider = None)
		
	else:
		provider = Provider.objects.get(id=id_provider)
		measurement = Measurement(idProvider = provider, datetime = datetime, readings = measurements_dict, idStation = None)
	measurement.save()

# Valida si el archivo f 
# tiene al menos min_length lineas
# retorna un boolean 
def is_valid_len(f,min_length):
	for i, l in enumerate(f):
		if i > min_length :
			return True
	return False