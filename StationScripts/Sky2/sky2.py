#!/usr/bin/python
import time
import urllib2 
import json
import time
import psycopg2
import datetime

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

	#Print Tables
	cursor.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
	print cursor.fetchall()

	print '\n\nPrint databases'	
	cursor.execute("""SELECT datname from pg_database""")
	rows = cursor.fetchall()
	print rows

	cursor.execute('Select * FROM "TimeSeries_stationtype"')
	rows = cursor.fetchall()
	for row in rows:
		print row
	dt = datetime.datetime(2018,8,4)
	myRead = str({'key1':1, 'key2':'value2'})
#	cursor.execute('Insert into "TimeSeries_stationtype" (brand, model, automatic) values (%s, %s, %s)', ("OneBrand", "OneModel", False))
#	myConnection.commit()
	cursor.execute('Insert into "TimeSeries_measurement" (datetime, idProvider) values (%s, %s)', (dt, 1)) 
	myConnection.close()
	return

	while(True):
		tokens = getTokens(filename)
		print tokens
		for token in tokens:
			request = urllib2.Request(API_URL)
			request.add_header('Authorization', token)
			response = urllib2.urlopen(request).read()
			json1_data = json.loads(response)[0]
			data = json1_data['Data']
			
			pressure = data['Pressure']
			luminance = data['Luminance']
			temperature = data['Temperature']
			voltage = data['Voltage']
			uvIndex = data['UVIndex']
			timestamp = data['TS']
			humidity = data['Humidity']
			rain = data['Rain']
			night = data['Night']
			imageUrl = data['ImageURL']

			print data

#			print 'Temperature: ' + str(json1_data['Data']['Temperature'])
		time.sleep(frequency)

hostname = 'localhost'
username = 'obayona'
password = 'EloyEcuador93'
database = 'resclima'

myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
FILENAME = './tokens//sky2tokens.txt'
FREQUENCY = 60*15
API_URL = 'https://api.bloomsky.com/api/skydata/.?unit=intl'
bloomsky_client(API_URL, FREQUENCY, FILENAME, myConnection)
exit()
