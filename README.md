# RESCLIMA

Plataforma para el manejo de datos geo-espaciales, series de tiempo y movilidad

Contenido:

- RESCLIMA/ 

Aplicacion web hecha en Django. 


- data/

Carpeta con datos de prueba


- ShapeEditor/

Es un proyecto en Django con la implementacion del upload y download de un shapefile (Va a ser eliminado)


-------------------------
# Dependencias
Django 1.8
postgres
postgis
gdal
mapnik
lxml
floppyforms

# Instrucciones instalacion de gdal:

$ sudo apt-get build-dep gdal

Descomprimir el archivo gdal-2.1.0.tar.gz (ubicado en el directorio raiz)

$ cd gdal-2.1.0/

$ ./configure  --prefix=/usr/ --with-python

$ make

$ sudo make install

$ cd swig/python/

$ sudo python setup.py install

Para comprobar si la instalacion fue correcta, en el interprete de python importar gdal:

from osgeo import ogr

# Configurar postgres

Crear un usuario en postgres; user: obayona, password: EloyEcuador93

Crear una base de datos "resclima"

Agregarle la extencion postgis

\c resclima;

CREATE EXTENSION postgis;

# Instalacion floppyforms
MapWidget. Para poder usar el Point Field Widget es necesario tener instalado django-floppyforms para una manipulacion mas facil de GEOS geometry fields:

$ pip install -U django-floppyforms

# Instalacion Mapnik

$ sudo pip install mapnik



