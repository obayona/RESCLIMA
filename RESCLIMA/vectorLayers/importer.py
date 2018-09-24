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
	categories_string = request.POST["categories_string"]


	# se verifica que esten unicamente los archivos requeridos
	# y que todos deben tener el mismo nombre
	required_extensions = [".shp", ".shx", ".dbf", ".prj"]
	has_extension = {}

	for extension in required_extensions:
		has_extension[extension] = False

	filename = None;
	for f in list_files:
		parts = os.path.splitext(f.name)
		# se obtiene el nombre y extension del archivo
		fname = parts[0].lower()
		extension = parts[1].lower()
		# se comprueba que todos los archivos se llamen igual
		if(filename==None):
			filename = fname
		elif(filename!=fname):
			result["error"] = "Todos los archivos deben tener el mismo nombre";
			return result;

		if extension in required_extensions:
			has_extension[extension] = True;
		else:
			result["error"] = "No se admite archivo con extension " + extension;
			return result;

	# se valida que los archivos requeridos existan
	for extension in required_extensions:
		if (not(has_extension[extension])):
			result["error"] = "Archivo perdido requerido ."+extension
			return result

	# se guardan los archivos en una carpeta temporal
	temp_dir = tempfile.mkdtemp()
	vectorlayer_name = filename + ".shp" # nombre del archivo shapefile
	
	for ftemp in list_files:

		# si el objeto ftemp de tipo UploadedFile, 
		# tiene el atributo: ftemp.file.name
		# significa que ftemp es una instancia de TemporaryUploadedFile
		# lo que siginifica que el archivo esta guardado en el disco.
		# Si ftemp no tiene el atributo: ftemp.file.name, 
		# ftemp es una instancia de InMemoryUploadedFile, 
		# lo que significa que los datos del archivo estan en memoria.
		# Si loas archivos ya estan en el disco, se los mueve hacia un directorio
		# temporal.
		# Si los archivos estan memoria, se los escribe en el disco dentro del
		# directorio temporal

		# nueva ubicacion del archivo
		ftemp_path_dst = os.path.join(temp_dir,ftemp.name)
		print ftemp_path_dst
		if (hasattr(ftemp,'temporary_file_path')):
			# el archivo ya esta en disco
			ftemp_path = ftemp.temporary_file_path()
			# mueve el archivo
			shutil.move(ftemp_path,ftemp_path_dst)
		else:
			# el archivo esta en memoria

			# se crea un archivo en el directorio temporal
			f = open(ftemp_path_dst, 'wb+')
			# se guardan los datos en el archivo	
			for chunk in ftemp.chunks():
				f.write(chunk)
			f.close()
				
		ftemp.close()

	# se llama a la tarea de celery
	# para que se ejecute asincronicamente
	vectorlayer_params = {}
	vectorlayer_params["temp_dir"] = temp_dir
	vectorlayer_params["vectorlayer_name"] = vectorlayer_name
	vectorlayer_params["encoding"] = encoding
	vectorlayer_params["title"] = title
	vectorlayer_params["abstract"] = abstract
	vectorlayer_params["date_str"] = date_str
	vectorlayer_params["categories_string"] = categories_string

	task = import_vector_layer.delay(vectorlayer_params)
	# se retorna el id task
	result["error"] = None
	result["task_id"] = task.id;
	return result;

