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

postgres 10

postgis

gdal

mapnik

lxml

floppyforms

TimescaleDB

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


# Instalacion Postgres 10

https://askubuntu.com/questions/1009975/unable-to-install-postgresql-10-on-ubuntu-16-04


# Instalacion Postgis

$ sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
$ sudo apt-get update
$ sudo apt-get install postgis

Se debe instalar PostGIS version 2.4.4


# Instala TimescaleDB

$ sudo add-apt-repository ppa:timescale/timescaledb-ppa
$ sudo apt-get update

Instalar para postgres 10:
$ sudo apt install timescaledb-postgresql-10

$ sudo nano /etc/postgresql/(postgres_version)/main/postgresql.conf

Localizar y descomentar la línea shared\_preload_libraries e igualarla a 'timescaledb'. 

Debe quedar:
shared\_preload_libraries = 'timescaledb'

$ sudo service postgresql restart



# Configurar postgres

Crear un usuario en postgres; debe coincidir con el usuario del archivo settings.py

Crear una base de datos "resclima"

\c resclima;

CREATE EXTENSION postgis; 

CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

Se debe ejcutar las migraciones de django:

$ python manage.py makemigrations
$ python manage.py migrate

Ahora se debe crear la hypertabla de timescaledb

Debido a que en timescaledb el primary key siempre debe contener el campo de tiempo,
se debe alterar la tabla

ALTER TABLE "timeSeries_measurement" ADD CONSTRAINT ts PRIMARY KEY (ts,id_m);

De esta manera, el primary key de la tabla "timeSeries_measurement" esta compuesto por (ts,id_m)
y la creacion del hypertable, no debe dar ningun problema

Cree el hypertable de la siguiente manera
SELECT create_hypertable('"timeSeries_measurement"','ts');


Para cargar datos iniciales en una tabla:

python manage.py loaddata TimeSeries/SensorTypes.json 


# Instalacion floppyforms
MapWidget. Para poder usar el Point Field Widget es necesario tener instalado django-floppyforms para una manipulacion mas facil de GEOS geometry fields:

$ pip install -U django-floppyforms

# Instalacion Mapnik

$ sudo pip install mapnik



