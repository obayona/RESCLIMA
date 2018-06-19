import time, threading, urllib2 

import json
import time

def getTokens(filename):
	f = open(filename)
	tokens = []
	for token_line in f:
		token_line = token_line.strip()
		if len(token_line) > 0:
			tokens.append(token_line)
	f.close()
	return tokens

def bloomsky_client(apiUrl, frequency, filename):
	while(True):
		tokens = getTokens(filename)
		print tokens
		for token in tokens:
			request = urllib2.Request(API_URL)
			request.add_header('Authorization', token)
			response = urllib2.urlopen(request).read()
			json1_data = json.loads(response)[0]
			print 'Temperature: ' + str(json1_data['Data']['Temperature'])
		time.sleep(frequency)

FILENAME = './tokens/tokens.txt'
FREQUENCY = 60*15
API_URL = 'https://api.bloomsky.com/api/skydata/.?unit=intl'
bloomsky_client(API_URL, FREQUENCY, FILENAME)

