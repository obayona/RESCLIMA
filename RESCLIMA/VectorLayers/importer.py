# -*- encoding: utf-8 -*-
import os 
import tempfile
import shutil
from tasks import import_vector_layer

# pendiente estilos
def import_data(request):
	# objeto con el resultado de la operacion
	result = {}

	# se obtienen las variables del POST
	list_files = request.FILES.getlist("import_files")
	encoding  = request.POST["encoding"]
	title = request.POST["title"]
	abstract = request.POST["abstract"]
	date_str = request.POST["data_date"]
	# se verifica que esten todos los archivos requeridos
	required_suffixes = [".shp", ".shx", ".dbf", ".prj"]
	has_suffix = {}
	for suffix in required_suffixes:
		has_suffix[suffix] = False

	for f in list_files:
		extension = os.path.splitext(f.name)[1].lower()
		if extension in required_suffixes:
			has_suffix[extension] = True

	for suffix in required_suffixes:
		if not has_suffix[suffix]:
			result["error"] = "Archivo perdido requerido ."+suffix
			return result

	# se guardan los archivos en una carpeta temporal
	temp_dir = tempfile.mkdtemp()
	vectorlayer_name = None # nombre del archivo shapefile
	
	for ftemp in list_files:

		# si el objeto ftemp de tipo UploadedFile, 
		# tiene el atributo: ftemp.file.name
		# significa que ftemp es una instancia de TemporaryUploadedFile
		# lo que siginifica que el archivo esta guardado en el disco.
		# Caso contrario, signfica ftemp es una instancia de
		# InMemoryUploadedFile, lo que significa que los datos del archivo
		# estan en memoria.
		# Si loas archivos ya estan en el disco, se los mueve hacia un directorio
		# temporal.
		# Si los archivos estan memoria, se los escribe en el disco dentro del
		# directorio temporal
		if (hasattr(ftemp,'temporary_file_path')):
			# el archivo ya esta en disco
			ftemp_path = ftemp.temporary_file_path()
			# nueva ubicacion
			ftemp_path_dst = os.path.join(temp_dir,ftemp.name)
			# mueve el archivo
			shutil.move(ftemp_path,ftemp_path_dst)
		else:
			# el archivo esta en memoria
			file_dir = os.path.join(temp_dir,ftemp.name)
			# se crea un archivo en el directorio temporal
			f = open(file_dir, 'wb+')
			# se guardan los datos en el archivo	
			for chunk in ftemp.chunks():
				f.write(chunk)
			f.close()

		if ftemp.name.endswith(".shp"):
			vectorlayer_name = ftemp.name
				
		ftemp.close()
	

	# se llama a la tarea de celery
	# para que se ejecute asincronicamente
	vectorlayer_params = {}
	vectorlayer_params["temp_dir"] = temp_dir
	vectorlayer_params["vectorlayer_name"] = vectorlayer_name;
	vectorlayer_params["encoding"] = encoding
	vectorlayer_params["title"] = title
	vectorlayer_params["abstract"] = abstract
	vectorlayer_params["date_str"] = date_str

	task = import_vector_layer.delay(vectorlayer_params);
	# se retorna el id task
	result["error"] = None
	result["task_id"] = task.id;
	return result;
