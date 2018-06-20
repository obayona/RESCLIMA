import configparser
from datetime import datetime
from dateutil.parser import parse
from TimeSeries.models import *
import os

def parseHOBO(file):
	"""Parse HOBO file"""
	STATION="HOBO"
	module_dir = os.path.dirname(__file__)
	config_file_path = os.path.join(module_dir, 'meteo_stations.cfg')
	config = configparser.ConfigParser()
	config.read(config_file_path)

	if "HOBO" not in config.sections():
		raise KeyError("Meteorological station not configured. Exit...") 
	headers = int (config.get(STATION,"headers"))
	#read verbose headers
	id_station = file.readline().split(":")
	id_station = id_station[1].strip()

	datetime_format = str(config.get(STATION,"datetime_format"))
	date_pos = int(config.get(STATION,"date_pos")) - 1

	lines = [line.rstrip('\n') for line in file]
	lines = lines[headers:]
	#start reading the file

	for line in lines:
		measures = line.strip().split("\t")
		print measures
		#Parse timestamp as it can be a datetime or date and time independent fields
		datetime = measures[date_pos]
		ts = parseDatetime(datetime)
		fields = config.get(STATION,"fields")
		fields = fields.strip().split(",")
		measures_num = len(measures)
		#form json of readings
		measures_dict = {}
		for i in range (2, measures_num):
			measures_dict[fields[i]] = measures[i]

		#save MeasureModel
		saveMeasurements(id_station,None,measures_dict, ts)
	
	return None
		

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
		measurement = Measurement(idStation = station, datetime = datetime, readings = measurements_dict)
	else:
		provider = Provider.objects.get(id=id_provider)
		measurement = Measurement(idProvider = provider, datetime = datetime, readings = measurements_dict)
	measurement.save()