from osgeo import ogr, osr
from django.contrib.gis.geos.collections import MultiPolygon, MultiLineString
from django.contrib.gis.geos.geometry import GEOSGeometry
import datetime
from lxml import etree

def ogr_type_to_geometry_name(ogr_type):
    return {ogr.wkbUnknown            : 'Unknown',
            ogr.wkbPoint              : 'Point',
            ogr.wkbLineString         : 'LineString',
            ogr.wkbPolygon            : 'Polygon',
            ogr.wkbMultiPoint         : 'MultiPoint',
            ogr.wkbMultiLineString    : 'MultiLineString',
            ogr.wkbMultiPolygon       : 'MultiPolygon',
            ogr.wkbGeometryCollection : 'GeometryCollection',
            ogr.wkbNone               : 'None',
            ogr.wkbLinearRing : 'LinearRing'}.get(ogr_type)

def wrap_geos_geometry(geometry):
    if geometry.geom_type == "Polygon":
        return MultiPolygon(geometry)
    elif geometry.geom_type == "LineString":
        return MultiLineString(geometry)
    else:
        return geometry

def calc_geometry_field(geometry_type):
    if geometry_type == "Polygon":
        return "geom_multipolygon"
    elif geometry_type == "LineString":
        return "geom_multilinestring"
    else:
        return "geom_" + geometry_type.lower()

def getOGRFeatureAttribute(attr, feature, encoding):
    attr_name = str(attr.name)
    if not feature.IsFieldSet(attr_name):
        return (True, None)
    needs_encoding = False
    if attr.type == ogr.OFTInteger:
        value = str(feature.GetFieldAsInteger(attr_name))
    elif attr.type == ogr.OFTIntegerList:
        value = repr(feature.GetFieldAsIntegerList(attr_name))
    elif attr.type == ogr.OFTReal:
        value = feature.GetFieldAsDouble(attr_name)
        value = "%*.*f" % (attr.width, attr.precision, value)
    elif attr.type == ogr.OFTRealList:
        values = feature.GetFieldAsDoubleList(attr_name)
        str_values = []
        for value in values:
            str_values.append("%*.*f" % (attr.width,
                                         attr.precision,
                                         value))
        value = repr(str_Values)
    elif attr.type == ogr.OFTString:
        value = feature.GetFieldAsString(attr_name)
        needs_encoding = True
    elif attr.type == ogr.OFTStringList:
        value = repr(feature.GetFieldAsStringList(attr_name))
        needs_encoding = True
    elif attr.type == ogr.OFTDate:
        parts = feature.GetFieldAsDateTime(attr_name)
        year,month,day,hour,minute,second,tzone = parts
        value = "%d,%d,%d,%d" % (year,month,day,tzone)
    elif attr.type == ogr.OFTTime:
        parts = feature.GetFieldAsDateTime(attr_name)
        year,month,day,hour,minute,second,tzone = parts
        value = "%d,%d,%d,%d" % (hour,minute,second,tzone)
    elif attr.type == ogr.OFTDateTime:
        parts = feature.GetFieldAsDateTime(attr_name)
        year,month,day,hour,minute,second,tzone = parts
        value = "%d,%d,%d,%d,%d,%d,%d,%d" % (year,month,day,
                                             hour,minute,
                                             second,tzone)
    elif attr.type== ogr.OFTInteger64:
        value = str(feature.GetFieldAsInteger64(attr_name))
    else:
        return (False, "Unsupported attribute type: " +
                       str(attr.type))
    if needs_encoding:
        try:
            value = value.decode(encoding)
        except UnicodeDecodeError:
            return (False, "Unable to decode value in " +
                    repr(attr_name) + " attribute.&nbsp; " +
                    "Are you sure you're using the right " +
                    "character encoding?")
    return (True, value)


def unwrap_geos_geometry(geometry):
    if geometry.geom_type in ["MultiPolygon","MultiLineString"]:
        if len(geometry) == 1:
            geometry = geometry[0]
    return geometry


def set_ogr_feature_attribute(attr, value, feature, encoding):
    attr_name = str(attr.name)
    if value == None:
        feature.UnsetField(attr_name)
        return
    if attr.type == ogr.OFTInteger:
        feature.SetField(attr_name, int(value))
    elif attr.type == ogr.OFTIntegerList:
        integers = eval(value)
        feature.SetFieldIntegerList(attr_name, integers)
    elif attr.type == ogr.OFTReal:
        feature.SetField(attr_name, float(value))
    elif attr.type == ogr.OFTRealList:
        floats = []
        for s in eval(value):
            floats.append(eval(s))
        feature.SetFieldDoubleList(attr_name, floats)
    elif attr.type == ogr.OFTString:
        feature.SetField(attr_name, value.encode(encoding))
    elif attr.type == ogr.OFTStringList:
        strings = []
        for s in eval(value):
            strings.append(s.encode(encoding))
        feature.SetFieldStringList(attr_name, strings)
    elif attr.type == ogr.OFTDate:
        parts = value.split(",")
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
        tzone = int(parts[3])
        feature.SetField(attr_name, year, month, day, 0, 0, 0, tzone)
    elif attr.type == ogr.OFTTime:
        parts = value.split(",")
        hour = int(parts[0])
        minute = int(parts[1])
        second = int(parts[2])
        tzone = int(parts[3])
        feature.SetField(attr_name, 0, 0, 0, hour, minute, second, tzone)
    elif attr.type == ogr.OFTDateTime:
        parts = value.split(",")
        year  = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
        hour = int(parts[3])
        minute = int(parts[4])
        second = int(parts[5])
        tzone = int(parts[6])
        feature.SetField(attr_name, year, month, day, hour, minute, second, tzone)
        

        

def getAttrValue(attr, value, encoding):
    attr_name = str(attr.name)
    if value == None:
        return value

    if attr.type == ogr.OFTInteger:
        return int(value);
    elif attr.type == ogr.OFTIntegerList:
        integers = eval(value)
        return integers
    elif attr.type == ogr.OFTReal:
        return float(value)
    elif attr.type == ogr.OFTRealList:
        floats = []
        for s in eval(value):
            floats.append(eval(s))
        return floats
    elif attr.type == ogr.OFTString:
        return value.encode(encoding)
    elif attr.type == ogr.OFTStringList:
        strings = []
        for s in eval(value):
            strings.append(s.encode(encoding))
        return strings
    elif attr.type == ogr.OFTWideString:
         return value.encode(encoding)
    elif attr.type == ogr.OFTDate:
        parts = value.split(",")
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
        tzone = int(parts[3])
        result = datetime.datetime(year=year,month=month,day=day,tzinfo=tzone);
        return result
    elif attr.type == ogr.OFTTime:
        parts = value.split(",")
        hour = int(parts[0])
        minute = int(parts[1])
        second = int(parts[2])
        tzone = int(parts[3])
        result = datetime.datetime(hour=hour,minute=minute,second=second,tzinfo=tzone);
        return result
    elif attr.type == ogr.OFTDateTime:
        parts = value.split(",")
        year  = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
        hour = int(parts[3])
        minute = int(parts[4])
        second = int(parts[5])
        tzone = int(parts[6])
        result = datetime.datetime(year=year,month=month,day=day,hour=hour,minute=minute,second=second,tzinfo=tzone)
        return result;
    elif attr.type==ogr.OFTInteger64:
         return int(value);
    elif attr.type == ogr.OFTInteger64List:
        integers = eval(value)
        return integers

    return None;

# retorna el bbox de una capa
# como poligono GEOSGeometry
def getLayerBBox(minX,minY,maxX,maxY):
    #se crea un anillo
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint_2D(minX,minY);
    ring.AddPoint_2D(minX,maxY);
    ring.AddPoint_2D(maxX,maxY)
    ring.AddPoint_2D(maxX,minY)
    ring.AddPoint_2D(minX,minY);
    # se crea el poligono
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)
    
    poly = GEOSGeometry(poly.ExportToWkt())
    return poly


# Transforma un archivo sld version 1.1.0 a 
# un archivo sld version 1.0.0
# recibe el contenido del archivo en un string
# retorna un string con el contendio del sld resultante

def transformSLD(sld):

    # Se crea un string con la cabecera
    new_sld = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
    new_sld = "<sld:StyledLayerDescriptor version=\"1.0.0\" "
    new_sld = new_sld + "xmlns:sld=\"http://www.opengis.net/sld\" "
    new_sld = new_sld + "xmlns:ogc=\"http://www.opengis.net/ogc\" "
    new_sld = new_sld + "xmlns:gml=\"http://www.opengis.net/gml\" "
    new_sld = new_sld + "xmlns:xlink=\"http://www.w3.org/1999/xlink\" "
    new_sld = new_sld + "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" "
    new_sld = new_sld + "xsi:schemaLocation=\"http://www.opengis.net/sld http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd\">"

    # con la libreria lxml se parsea el string sld
    root = etree.fromstring(sld);
    # se obtienen los hijos del root
    children = root.getchildren();

    # en el string children_str se agregan los hijos
    children_str = ""
    for child in children:
        children_str = children_str + etree.tostring(child);
    
    # se agrega el string de los hijos a la cabecera
    new_sld = new_sld + children_str
    # se cierra el ultimo tag
    new_sld = new_sld + "</sld:StyledLayerDescriptor>"

    # se reemplazan los prefix "se" por "sld"
    new_sld = new_sld.replace("se:","sld:");
    # se reemplazan los prefix "SvgParameter" por "CssParameter" 
    new_sld = new_sld.replace("SvgParameter","CssParameter");

    
    return new_sld