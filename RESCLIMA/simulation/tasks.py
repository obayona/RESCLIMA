# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

from celery import shared_task
from celery_progress.backend import ProgressRecorder
import traceback
import time
import json
import os, sys, errno
import subprocess
import shutil

from django.conf import settings

@shared_task(bind=True)
def simulation_task(self, params):
	# PATH sumocfg, Step de la simulacion
	SUMO_HOME = "/usr/share/sumo"
	progress_recorder = ProgressRecorder(self)
	sumo_parameters = '/home/manuel/Desktop/DATACITY/RESCLIMA/simulation/sumoparams.json'
	sumoParams = None
	with open(sumo_parameters) as data_file:
		sumoParams = json.load(data_file)

	try:
		#os.environ["SUMO_HOME"] = "/home/fernando/sumo-git"
		os.environ["SUMO_HOME"] = SUMO_HOME
		tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
		sys.path.append(tools)
		import sumolib
		import traci as traci
		MEDIA = settings.MEDIA_ROOT
		try:
		  path = os.path.join(MEDIA + params['simulation_path'], 'output')
		  os.mkdir(path)
		except OSError as e:
		  if e.errno != errno.EEXIST:
			  return os.path.join(MEDIA + params['simulation_path'], 'output')
		  return os.path.join(MEDIA + params['simulation_path'], 'output')
		PATH = MEDIA + params['simulation_whole_path']
		# Definiendo las salidas de la simulacion
		TRACE_OUT = MEDIA + params['simulation_path'] + "output/resclima_trace_output.xml"
		EMISSION_OUT = MEDIA + params['simulation_path'] + "output/resclima_emission_output.xml"
		SUMMARY_OUT = MEDIA + params['simulation_path'] + "output/resclima_summary_output.xml"
		# Definiendo la ruta del simulador y realizar la simulacion
		#sumoBinary = "/home/fernando/sumo-git/bin/sumo"
		sumoBinary = sumoParams["sumoBinary"]
		sumoCmd = [sumoBinary, "-c", PATH, "--fcd-output", TRACE_OUT, "--emission-output", EMISSION_OUT, "--summary", SUMMARY_OUT]
		traci.start(sumoCmd, port=8888)
		print("Realizando la simulacion...")
		step = 0
		while step < params['simulation_step']:
			traci.simulationStep()
			# Your Simulation Script here
			print("Step:" + str(step))
			step += 1
			time.sleep(1)
			progress_recorder.set_progress(step, params['simulation_step'])
		traci.close()
		print("¡La simulacion ha terminado con exito!")
	except ImportError as e:
		traceback.print_exc()
		return 	e + params['simulation_path']	

	return '¡La simulacion ha terminado con exito!' 