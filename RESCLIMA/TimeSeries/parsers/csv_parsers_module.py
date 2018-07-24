import configparser
from datetime import datetime
from dateutil.parser import parse
from TimeSeries.models import *
import os

__ERROR_MESSAGES__ = {
	"uknown_station": "uknown station - not in config file", 
	"no_station_id": "No id in HOBO-MX2300 file",
	"invalid_len": "File is too small",
	"user_menssage": "Error al procesar su archivo",
	"no_columns": "Not enough columns"
}

def parseHOBO(file):
	"""Parse HOBO file"""
	global __ERROR_MESSAGES__
	STATION="HOBO"
	#check file length
	if valid_len(file) == False:
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
	
	#read id of station in the first line
	id_station = file.readline().split(":")
	if len(id_station) < 2 :
		print(__ERROR_MESSAGES__["no_station_id"])
		return (__ERROR_MESSAGES__["user_message"])
	
	id_station = id_station[1].strip()
	datetime_format = str(config.get(STATION,"datetime_format"))
	date_pos = int(config.get(STATION,"date_pos")) - 1

	#pass all the headers
	for i in range (headers):
		file.readline()

	#start reading the file
	for line in lines:
		measures = line.strip().split("\t")
		measures_num = len(measures)
		fields = config.get(STATION,"fields")
		fields = fields.strip().split(",")
		if measures_num != len(fields):
			min_len = len(fields) if len(fields)<measures_num else measures_num
		if min_len < 1:
			print (__ERROR_MESSAGES__["no_columns"])
			return (__ERROR_MESSAGES__["user_message"])

		#Parse timestamp as it can be a datetime or date and time independent fields
		datetime = measures[date_pos]
		ts = parseDatetime(datetime)
		
		#form json of readings
		measures_dict = {}
		#traverse each line of the file starting after de column of datetime
		for i in range (date_pos+1, min_len):
			measures_dict[fields[i]] = measures[i]

		#save MeasureModel
		saveMeasurements(id_station,None,measures_dict, ts)
		
	return "Success"
		

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



def saveMeasurements(id_station,id_provider,measurements_dict,datetime = datetime.now()):

	if id_provider == None and id_station!= None:
		station = Station.objects.get(serialNum=id_station);
		measurement = Measurement(idStation = station, datetime = datetime, readings = measurements_dict, idProvider = None)
		
	else:
		provider = Provider.objects.get(id=id_provider)
		measurement = Measurement(idProvider = provider, datetime = datetime, readings = measurements_dict, idStation = None)
	measurement.save()

def valid_len(f):

	for i, l in enumerate(f):
		pass
		if i > 4 :
			return True
	return False