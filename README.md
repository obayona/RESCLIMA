# RESCLIMA

ShapeEditor/ 
Es un proyecto en Django con la implementacion del upload y download de un shapefile

En ShapeEditor/datos
Hay shapefiles (zipped) para probar el upload. Los shapefiles se pueden abrir con QGIS.
En el upload solo funciona ALG-0.zip (hay que revisar los errores)
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
Para descargar un shapefile, click en el link: "Export", (probar con los ultimos elementos de la lista, los primeros tienen error)


-------------------
Tareas:
-Oswaldo
1) Mejorar la subida del shapefile, hacerla transaccional, porque si algo falla en el proceso
quedan registros en la tabla shapefile, mientras que las otras tablas quedan vacias.
2) Implementar un visor para los datos vectoriales, que se obtienen con el queryset de django
3) Averiguar como calcular el BBOX de los datos vectoriales, de la tabla Features

-Viviana
1) Implementar la app "Sensors" o "TimeSeries" o cualquier nombre. Se la puede hacer en un proyecto aparte y luego lo combinamos, cuando tenga bien hecha la subida y bajada de shapefiles
2) Dentro de la app "Sensors" implementar el modelo con las tablas: Sensor, mesurements, variables, etc. El tipo de dato punto seria este tipo de dato: models.PointField(srid=4326,blank=True,null=True), aunque hay que ver que es mas conveniente.
3)  Implementar un visor para los datos vectoriales, que se obtienen con el queryset de django. La idea es visualizar los puntos (ubicaciones) de los sensores.
Y que al dar click en un punto, se muestre la serie de tiempo. Este punto es mas para probar las tecnologias, el objetivo no es tener el visor definitivo. Este punto se parace al punto 2 de mis tareas, porque ambos deberiamos buscar como hacer eso, y al primero que le salga le dice al otro, se puede probar las librerias OpenLayers o Leaftlet.
4) Implementar la tabla metadatos. La idea es que cada vez que se suba un shapefile o que se modifique las tablas del modelo de Sensors, se crea un registro en metadata.
Este punto se lo puede hacer cuando regreses porque hay que revisar bien como hacemos. Además debe ser una operacion transaccional.
