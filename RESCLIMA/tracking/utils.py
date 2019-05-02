from osgeo import ogr
from lxml import etree

#Genera un archivo gpx y lo guarda en memoria
#a partir de valores de lonlat guardados en la base
#gpx es un diccionario con valores del nombre, la latitud,
#longitud iniciales, elevacion
def generateGPx(lonlat, gpx):

    new_gpx = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
    new_gpx = "<gpx version=\"1.0\">"
    new_gpx = new_gpx + "<name>"+gpx.name+"</name>"
    new_gpx = new_gpx + "<wpt lat='"+gpx.lat+"'lon='"+gpx.lon+"'>"
    new_gpx = new_gpx + "<ele>"+gpx.ele+"</ele>"
    new_gpx = new_gpx + "<name>"+gpx.name+"</name> </wpt>"
    new_gpx = new_gpx + "<trk><name>"+gpx.name+"</name><number>1</number><trkseg>"
    
    for lon, lat, ele, time in lonlat.items():
        new_gpx = new_gpx + "<trkpt lat='"+lon+"' lon='"+lat+"'><ele>"+ele+"</ele><time>"+time+"</time></trkpt>"

    new_gpx = new_gpx + "</trkseg></trk></gpx>"

    return new_gpx

# Toma los valores de track de un sensor si coincide dentro de 
# las fechas especificas y agrega o elimina valores de longitud,
# latitud y elevacion y actualiza el nombre del archivo
def updateGPx(lonlat, gpx):
    return 0
    



