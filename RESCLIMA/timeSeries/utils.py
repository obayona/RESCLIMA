# -*- encoding: utf-8 -*-

from timeSeries.models import Variable,Station,Measurement,Provider
import pytz

# cuenta las lineas de un archivo
def count_file_lines(f):
	count_lines = len(f.readlines())
	f.seek(0)
	return count_lines

# parsea una medicion segun su tipo de dato
def parseMeasure(measure,datatype):
	if(datatype=="float"):
		return float(measure);
	elif(datatype=="string"):
		return measure;
	else:
		return None;

def transformToUTC(dt,local_tz_str):
	if(local_tz_str=="UTC"):
		return dt
	local_tz = pytz.timezone (local_tz_str);
	dt_with_tz = local_tz.localize(dt, is_dst=None)
	dt_in_utc = dt_with_tz.astimezone(pytz.utc)
	return dt_in_utc;

# guarda una medicion en la base de datos
def saveMeasurements(station,id_provider,measurements_dict,date_time):

	if id_provider == None and station!= None:
		measurement = Measurement(idStation = station, ts = date_time, readings = measurements_dict, idProvider = None)
	else:
		provider = Provider.objects.get(id=id_provider)
		measurement = Measurement(idProvider = provider, ts = date_time, readings = measurements_dict, idStation = None)
	measurement.save()
