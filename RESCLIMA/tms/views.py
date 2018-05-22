from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
import traceback
import math
import mapnik

MAX_ZOOM_LEVEL = 10
TILE_WIDTH     = 256
TILE_HEIGHT    = 256

def root(request):
	try:
		baseURL = request.build_absolute_uri()
		xml = []
		xml.append('<?xml version="1.0" encoding="utf-8" ?>')
		xml.append('<Services>')
		xml.append('<TileMapService title="RESCLIMA TMS" ' +
		       'version="1.0" href="' + baseURL + '1.0"/>')
		xml.append('</Services>')
		return HttpResponse("\n".join(xml), content_type="text/xml")
	except:
		traceback.print_exc()
		return HttpResponse("Error")

def service(request, version):
	try:
		if version != "1.0":
			raise Http404
		baseURL = request.build_absolute_uri()
		xml = []
		xml.append('<?xml version="1.0" encoding="utf-8" ?>')
		xml.append('<TileMapService version="1.0" services="' + baseURL + '">')
		xml.append('<Title>RESCLIMA TMS</Title>')
		xml.append('<Abstract></Abstract>')
		xml.append('<TileMaps>')
		
		id = str(1)
		xml.append('<TileMap title="' + "Prect" + '"')
		xml.append('srs="EPSG:4326"')
		xml.append('href="'+baseURL+'/'+id+'"/>')
		
		xml.append('</TileMaps>')
		xml.append('</TileMapService>')
		return HttpResponse("\n".join(xml), content_type="text/xml")
	except:
		traceback.print_exc()
	return HttpResponse("Error")

def tileMap(request, version, shapefile_id):
	if version != "1.0":
		raise Http404

	try:
		baseURL = request.build_absolute_uri()
		xml = []
		xml.append('<?xml version="1.0" encoding="utf-8" ?>')
		xml.append('<TileMap version="1.0" ' +
		           'tilemapservice="' + baseURL + '">')
		xml.append('<Title>' + "prect" + '</Title>')
		xml.append('<Abstract></Abstract>')
		xml.append('<SRS>EPSG:4326</SRS>')
		xml.append('<BoundingBox minx="-180" miny="-90" maxx="180" maxy="90"/>')
		xml.append('<Origin x="-180" y="-90"/>')
		xml.append('<TileFormat width="' + str(TILE_WIDTH) +
		           '" height="' + str(TILE_HEIGHT) + '" ' +
		           'mime-type="image/png" extension="png"/>')
		xml.append('<TileSets profile="global-geodetic">')
		
		for zoomLevel in range(0, MAX_ZOOM_LEVEL+1):
			unitsPerPixel = _unitsPerPixel(zoomLevel)
			xml.append('<TileSet href="' + 
			           baseURL + '/' + str(zoomLevel) +
			           '" units-per-pixel="'+str(unitsPerPixel) +
			           '" order="' + str(zoomLevel) + '"/>')
		xml.append('</TileSets>')
		xml.append('</TileMap>')
		return HttpResponse("\n".join(xml), content_type="text/xml")
	except:
		traceback.print_exc()
		return HttpResponse("Error")

def tile(request, version, shapefile_id, zoom, x, y):
	try:
		if version != "1.0":
			raise Http404
	
		zoom = int(zoom)
		x    = int(x)
		y    = int(y)

		if zoom < 0 or zoom > MAX_ZOOM_LEVEL:
			raise Http404

		xExtent = _unitsPerPixel(zoom) * TILE_WIDTH
		yExtent = _unitsPerPixel(zoom) * TILE_HEIGHT
		minLong = x * xExtent - 180.0
		minLat  = y * yExtent - 90.0
		maxLong = minLong + xExtent
		maxLat  = minLat  + yExtent

		if (minLong < -180 or maxLong > 180 or minLat < -90 or maxLat > 90):
			raise Http404

		map = mapnik.Map(TILE_WIDTH, TILE_HEIGHT,"+proj=longlat +datum=WGS84")
		map.background = mapnik.Color("#00000000")

		#capa raster
		raster = mapnik.Layer("raster");
		raster.datasource = mapnik.Gdal(file="/home_local/obayona/rasters/PRECT2018-05-21-21-39-21.tif");
		style = mapnik.Style()
		rule = mapnik.Rule()
		rule.symbols.append(mapnik.RasterSymbolizer())
		style.rules.append(rule)
		map.append_style("estilo",style)
		raster.styles.append("estilo")
		map.layers.append(raster)

		map.zoom_to_box(mapnik.Box2d(minLong, minLat, maxLong, maxLat))
		image = mapnik.Image(TILE_WIDTH, TILE_HEIGHT)
		mapnik.render(map, image)
		imageData = image.tostring('png')
    
		return HttpResponse(imageData, content_type="image/png")

	except:
		traceback.print_exc()
		return HttpResponse("Error")

def _unitsPerPixel(zoomLevel):
    return 0.703125 / math.pow(2, zoomLevel)