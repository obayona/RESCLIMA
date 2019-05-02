import subprocess
from celery import shared_task, current_task
import RESCLIMA.settings as settings
import os
from celery_progress.backend import ProgressRecorder

'''
Sube los valores de un archivo de transmision de datos
de trafico y guarda los valores de lon lat, elev para
crear un archivo gpx, para facilitar la graficacion de 
rutas en fechas especificas
'''
@shared_task
def save_traffic_data_file(values, current_name):
	progress_recorder = ProgressRecorder(self)
	full_path = settings.TEMPORARY_FILES_PATH
	full_name = os.path.join(full_path, current_name)
	result = {}
	# se actualiza el progreso 5%
	result["error"]=None
	result["percent"]=5
	current_task.update_state(state='PROGRESS',meta=result)
	
	with open(full_name,"w+") as output_file:
		for line in output_file:
			output_file.write(line)
    
	result["error"]=None
	result["percent"]=100
	current_task.update_state(state='PROGRESS',meta=result)
	return result