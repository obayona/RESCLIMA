#!/usr/bin/python
import time
import urllib2 
import json
import time
from datetime import datetime
import psycopg2
import logging
from threading import Condition, Thread
from Queue import Queue

# Script que descarga los datos
# de las estaciones SKY2 y las guarda en 
# la base de datos

# archivos de configuracion, log y backup
configFileName = "/home/manager/RESCLIMA/StationScripts/Sky2/config.json";
logFileName = "/home/manager/RESCLIMA/StationScripts/Sky2/log.txt"
backupFileName = "/home/manager/RESCLIMA/StationScripts/Sky2/backup.txt";

# variable de condicion
# para dormir el main
cv = Condition()
# cola para escribir en el archivo
# de backup
writeQueue = Queue()

def backup(measurement):
	measurement = measurement + "\n"
	writeQueue.put(measurement)
	outFile = open(backupFileName,'a')
	while writeQueue.qsize():
		outFile.write(writeQueue.get())
	outFile.flush()
	outFile.close()


def getVariablesByAliases(dbParams,variables_aliases):
	variables = []
	conn = None
	try:
		conn = psycopg2.connect(host="localhost",
								user=dbParams["user"],
								password=dbParams["password"],
								dbname=dbParams["dbname"]);
		cursor = conn.cursor()

		query = """
				SELECT v.id,v.alias,v.datatype
	            FROM \"TimeSeries_variable\" as v  
	            WHERE v.alias=%s
	            """;
		for variable_alias in variables_aliases:
			cursor.execute(query,(variable_alias,));
			result = cursor.fetchone();
			variable = {}
			variable["id"] = result[0];
			variable["alias"] = result[1];
			variable["datatype"] = result[2];
			variables.append(variable);

	except Exception as e:
		error_str = "Fallo la base de datos" + str(e);
		return None,error_str;
	finally:
		if conn:
			conn.close()

	return variables,None 

def getStations(dbParams):
	stations = []
	conn = None
	try:
		conn = psycopg2.connect(host="localhost",
								user=dbParams["user"],
								password=dbParams["password"],
								dbname=dbParams["dbname"]);
		cursor = conn.cursor()

		query = """
				SELECT s.id,s.token,s.frequency
                FROM \"TimeSeries_station\" as s,   
                \"TimeSeries_stationtype\" as st 
                WHERE st.brand='BloomSky' and st.model='SKY2' 
                and \"stationType_id\"=st.id
                """
		
		cursor.execute(query);
		results = cursor.fetchall();
		for row in results:	
			station = {}
			station["id"] = row[0];
			station["token"] = row[1];
			station["frequency"] = row[2];
			stations.append(station);

	except Exception as e:
		error_str = "Fallo la base de datos " + str(e);
		return None,error_str;
	finally:
		if conn:
			conn.close()

	return stations,None 

def getSKY2Data(token):
	try:
		url = 'https://api.bloomsky.com/api/skydata/.?unit=intl'
		request = urllib2.Request(url)
		request.add_header('Authorization', token)
		response = urllib2.urlopen(request).read()
		return response,None
	except Exception as e:
		error_str = "Error al descargar datos " + str(e)
		return None,error_str

def parseMeasurements(idStation,data,variables):
	source = json.loads(data)[0]
	readings = source['Data']
	timestamp = readings['TS']
	dt = datetime.utcfromtimestamp(timestamp)	
	timestamp_str = dt.strftime("%Y-%m-%d %H:%M:%S")


	result = {}
	for variable in variables:
		idVariable = variable["id"];
		alias = variable["alias"];
		result[idVariable] = readings[alias];

	values = json.dumps(result);
	measurement = {}
	measurement["idStation"]=idStation
	measurement["datetime"]=timestamp_str
	measurement["values"]=values
	return measurement, None

def insertMeasures(dbParams,measurements):
	conn = None
	try:
		conn = psycopg2.connect(host="localhost",
								user=dbParams["user"],
								password=dbParams["password"],
								dbname=dbParams["dbname"]);
		cursor = conn.cursor()
		query = "SELECT InsertSky2Measurements(%s::integer,%s::timestamp,%s::json)"
		idStation = measurements["idStation"]
		timestamp_str = measurements["datetime"]
		values = measurements["values"]
		cursor.execute(query,(idStation,timestamp_str,values,));
		conn.commit()
	except Exception as e:
		error_str = "Fallo la base de datos " + str(e);
		return error_str;
	finally:
		if conn:
			conn.close()

	return None 

def dataExtraction_thread(dbParams,station,variables):
	idStation = station["id"]
	token = station["token"]
	frequency = station["frequency"]
	seconds = frequency*60

	while(True):
		time.sleep(seconds)
		data,error = getSKY2Data(token);
		if(error):
			logging.error(error)
			continue
		measurements,error = parseMeasurements(idStation,data,variables)
		if(error):
			logging.error(error)
			continue
		error = insertMeasures(dbParams,measurements) 
		if(error):
			logging.error(error)
			# intenta guardar en el backup
			m_dump = json.dumps(measurements)
			backup(m_dump);


if __name__ == "__main__":
	
	# se inicializa el logger
	logging.basicConfig(filename=logFileName,
						format='%(asctime)s %(message)s')
	logging.debug('Adaptador SKY2 inicializado')

	
	# Se otienen las credenciales de 
	# la base de datos
	dbParams = None
	with open(configFileName) as f:
		dbParams = json.load(f)

	# se crea el arreglo de alias
	# de las variables
	variables_aliases = [];
	variables_aliases.append("Luminance");
	variables_aliases.append("Temperature");
	variables_aliases.append("Humidity");
	variables_aliases.append("ImageURL");
	variables_aliases.append("Rain");
	variables_aliases.append("Humidity");
	variables_aliases.append("Pressure");
	variables_aliases.append("Voltage");
	variables_aliases.append("Night");
	variables_aliases.append("UVIndex");


	variables,error = getVariablesByAliases(dbParams,variables_aliases);
	if(error):
		logging.error(error)
		exit(-1);

	stations,error = getStations(dbParams);

	if(error):
		logging.error(error)
		exit(-1);


	for station in stations:
		thread_ = Thread(target=dataExtraction_thread, args=(dbParams,station,variables,));
		thread_.setDaemon(True)
		thread_.start()

	cv.acquire()
	cv.wait()
