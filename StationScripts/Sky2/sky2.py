#!/usr/bin/python
import time
import urllib2 
import json
import time
import psycopg2
import datetime

# Script que descarga los datos
# de las estaciones SKY2 y las guarda en 
# la base de datos

"""
def getTokens(filename):
	f = open(filename)
	tokens = []
	for token_line in f:
		token_line = token_line.strip()
		if len(token_line) > 0:
			tokens.append(token_line)
	f.close()
	return tokens

def bloomsky_client(apiUrl, frequency, filename, myConnection):
	cursor = myConnection.cursor()
	while(True):
		tokens = getTokens(filename)
		for line in tokens:
			line = line.strip()
			fields = line.split(',')
			idStation = fields[0]
			token = fields[1]
			print token 
			request = urllib2.Request(API_URL)
			request.add_header('Authorization', token)
			response = urllib2.urlopen(request).read()
			json1_data = json.loads(response)[0]
			print json1_data,response
			readings = json1_data['Data']
			timestamp = readings['TS']
			dt = datetime.datetime.fromtimestamp(timestamp)
			cursor.execute('Insert into "TimeSeries_measurement" ("datetime", "idStation_id", "readings") values (%s, %s, %s)', (dt, idStation, str(readings)))
			myConnection.commit()
		time.sleep(frequency)
HOSTNAME = 'localhost'
USERNAME = 'obayona'
PASSWORD = 'EloyEcuador93'
DATABASE = 'resclima'

myConnection = psycopg2.connect( host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE )
FILENAME = 'tokens.txt'
FREQUENCY = 60*15
API_URL = 'https://api.bloomsky.com/api/skydata/.?unit=intl'
bloomsky_client(API_URL, FREQUENCY, FILENAME, myConnection)
myConnection.close()
"""

def getVariablesByAliases(dbParams,variables_aliases):
	conn = psycopg2.connect(host="localhost",
							user=dbParams["user"],
							password=dbParams["password"],
							dbname=dbParams["dbname"]);
	cursor = conn.cursor()

	variables = []
	for variable_alias in variables_aliases: 
		


if __name__ == "__main__":
	# archivos de configuracion, log y backup
	configFileName = "/home_local/obayona/Documents/RESCLIMA/StationScripts/Sky2/config.json";
    logFileName = "/home_local/obayona/Documents/RESCLIMA/StationScripts/Sky2/log.txt";
    backupFileName = "/home_local/obayona/Documents/RESCLIMA/StationScripts/Sky2/backup.txt";
    # se registran los signal
    

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

    variables,error = getVariablesByAliases(dbParams,variables_aliases);
