import os, os.path, tempfile, zipfile
import shutil, traceback
from osgeo import ogr
from django.contrib.gis.geos.geometry import GEOSGeometry
from osgeo import osr
from django.http import HttpResponse
from wsgiref.util import FileWrapper
import simplejson as json

def export_gpxfile(path):
    wrapper = FileWrapper(open(path,"rb"))
    response = HttpResponse(wrapper, content_type='application/gpx')
    response['Content-Disposition'] = 'attachement; filename=dump.gpx'
    return response