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
	while(True):
		tokens = getTokens(filename)
		for line in tokens:
			line = line.strip()
			fields = line.split(',')
			idStation = fields[0]
			token = fields[1] 
			request = urllib2.Request(API_URL)
			request.add_header('Authorization', token)
			response = urllib2.urlopen(request).read()
			json1_data = json.loads(response)[0]
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
FILENAME = './tokens//sky2tokens.txt'
FREQUENCY = 60*15
API_URL = 'https://api.bloomsky.com/api/skydata/.?unit=intl'
bloomsky_client(API_URL, FREQUENCY, FILENAME, myConnection)
myConnection.close()
