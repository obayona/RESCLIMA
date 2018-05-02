# RESCLIMA

ShapeEditor/ 

Es un proyecto en Django con la implementacion del upload y download de un shapefile


En ShapeEditor/datos

Hay shapefiles (zipped) para probar el upload. Los shapefiles se pueden abrir con QGIS. El upload del archivo indonesia.zip funciona, pero hay que probar si se guardaron bien los datos, porque tiene atributos de tipo OFTInteger64. 

-------------------------
Instrucciones para shapeEditor:

Instalar las dependencias de GeoDjango, las mas importantes son: postgres con postgis, gdal

Crear un usuario en postgres; user: obayona, password: EloyEcuador93

-------------------------
Pasos para instalar gdal:

$ sudo apt-get build-dep gdal

Descomprimir el archivo gdal-2.1.0.tar.gz

$ cd gdal-2.1.0.tar.gz

$ ./configure  --prefix=/usr/ --with-python

$ make

$ sudo make install

$ cd swig/python/

$ sudo python setup.py install

Para comprobar si la instalacion fue correcta, en el interprete de python importar gdal:

from osgeo import ogr

--------------
Probar proyecto ShapeEditor:

$ python manage runserver

ir a localhost:8000/editor

Click en el boton "Import New Shapefile" 

Para descargar un shapefile, click en el link: "Export"

-------------------------
MapWidget/

Para poder usar el Point Field Widget es necesario tener instalado django-floppyforms para una manipulacion mas facil de GEOS geometry fields:

$ pip install -U django-floppyforms

Add floppyforms to your INSTALLED_APPS
