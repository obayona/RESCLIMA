import configparser
from datetime import datetime
from dateutil.parser import *
from TimeSeries.models import *

def parseHOBO(file):
	"""Parse HOBO file"""
	STATION="HOBO"
	config = configparser.ConfigParser()
	config.read("meteo_stations.cfg")
	if "HOBO" not in config.sections():
		raise KeyError("Meteorological station not configured. Exit...") 
	headers= int (config.get(STATION,"headers"))
	#read verbose headers
	id_sensor = file.readline().split(":")
	id_sensor = id_sensor[1].strip()
	file.readline()
	#start reading the file
	for line in file:
		measures = line.strip().split("\t")
		#Parse timestamp as it can be a datetime or date and time independent fields
		datetime_format = str(config.get(STATION,"datetime_format"))
		date_pos = int(config.get(STATION,"date_pos"))-1
		datetime = measures[date_pos - 1]
		ts = parseDatetime(datetime)
		fields = config.get(STATION,"fields")
		fields = fields.strip().split(",")
		measures_num = len(measures)
		#form json of readings
		measures_dict = {}
		for i in range (2, measures_num):
			measures_dict[fields[i]] = measures[i]

		#save MeasureModel
		saveMeasurements(null, id_sensor, ts, measures_dict)
	
		

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
		print measures 
		print "\n"

def parseDatetime(date, time = None):
	if time != None:
		date = date.strip()
		time = time.strip()
		ts = parse(date+" "+time)
	else:
		ts = parse(date)
	return ts



def saveMeasurements(id_provider = null, id_station = null, datetime = datetime.datetime.now(),measurements_dict):
	if id_provider = null:
		measurement = Measurement(idStation = id_station, datetime = datetime, readings = measurements_dict)
	else:
		measurement = Measurement(idProvider = id_provider, datetime = datetime, readings = measurements_dict)
	measurement.save()


	    

