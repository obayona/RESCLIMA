import mapnik
from lxml import etree
import traceback

def parseRasterSLD(sld):
	root = etree.fromstring(sld);
	xpath = "sld:UserLayer/sld:UserStyle/sld:FeatureTypeStyle/"
	xpath = xpath + "sld:Rule/sld:RasterSymbolizer/sld:ColorMap"
	colorMaps = root.findall(xpath,namespaces={"sld":"http://www.opengis.net/sld"})
	
	if (len(colorMaps)==0):
		return None
	
	colorMap = colorMaps[0]

	try:
		result = []
		for x in colorMap:
			entry = {}
			entry["color"] = x.get("color")
			entry["label"] = x.get("label")
			entry["opacity"] = x.get("opacity")
			entry["quantity"] = float(x.get("quantity"))
			result.append(entry)
	except:
		traceback.print_exc()
		return None

	return result