var vector_layer = undefined;


function createLegendRow(value,symbolizer){
	var row = document.createElement("div");
	
	var text = document.createElement("h4");
	text.innerHTML = value;

	var symb = document.createElement("div");
	var polygon = symbolizer.Polygon;
	symb.style.width = "20px";
	symb.style.height = "20px";
	symb.style.backgroundColor = polygon.fillColor;
	symb.style.borderWidth = polygon.strokeWidth;
	symb.style.borderColor = polygon.strokeColor;


	row.appendChild(symb);
	row.appendChild(text)
	return row;
}

function renderLegend(container_legend,rules){
	var container = document.getElementById(container_legend);
	container.innerHTML = "";

	var property;
	var i = 0; length = rules.length;


	for (i;i<length;i++){
		var rule = rules[i];
		property = rule.filter.property;
		var value = rule.filter.value;
		var symbolizer = rule.symbolizer;
		var row = createLegendRow(value,symbolizer);
		container.appendChild(row);
	}
	var prop = document.createElement("h2");
	prop.innerHTML = property;
	container.insertBefore(prop,container.firstChild);

}



function applyStyle(sld){
	var format = new OpenLayers.Format.SLD();
	var sld = format.read(sld);
	var styles = sld.namedLayers["map"].userStyles;
	var style = styles[0];
	vector_layer.styleMap.styles["default"] = style;
	vector_layer.redraw();

	renderLegend("legend",style.rules);
}


function requestStyle(style_id){
	var url = "/vector/export_style/" + style_id;
	var request = $.get(url);
	request.done(function(sld){
		applyStyle(sld)
	})
}


function cleanStyleList(styles_container){
	var selector = "#"+styles_container+ " > ul > li";
	var styles = document.querySelectorAll(selector);

	for (var i=0; i < styles.length; i++){
		style = styles[i]
		console.log("limpio", style.dataset.id)
		style.className = "list-group-item";
	}
}

function enabledStyle(styles_container){

	var selector = "#"+styles_container+ " > ul > li";
	var styles = document.querySelectorAll(selector);

	for (var i=0; i < styles.length; i++){
		style = styles[i]
		style_id = style.dataset.id;

		
		if(i==0){
			style.className = "list-group-item active";
			requestStyle(style_id);
		}
		else{
			style.className = "list-group-item";
		}


		style.addEventListener("click",function(event){
			var target = event.target;
			style_id = target.dataset.id;
			requestStyle(style_id);
			cleanStyleList(styles_container)
			target.className = "list-group-item active";
		});

	}

}


function initMap(map_container){
	var map = new OpenLayers.Map({
		div:map_container,
		projection:"EPSG:3857",
		displayProjection: new OpenLayers.Projection("EPSG:4326"),
		numZoomLevels:11,
		units: 'm'
	});
	var osm = new OpenLayers.Layer.OSM("OSM");
	map.addLayer(osm);
	map.zoomToMaxExtent();
	return map;
}


function renderFeatureLayer(data,map){

	var lon = data.centroid.lon;
	var lat = data.centroid.lat;
   	var zoom = 4;
   	map.setCenter(new OpenLayers.LonLat(lon, lat).transform('EPSG:4326','EPSG:900913'), zoom);

	var geojson_format = new OpenLayers.Format.GeoJSON();
	vector_layer = new OpenLayers.Layer.Vector({projection: new OpenLayers.Projection("EPSG:900913")});
	var features = geojson_format.read(data);
	
	for (i=0; i<features.length; i++){
		feature = features[i];
		feature.geometry.transform('EPSG:4326','EPSG:900913');
   	}

   	vector_layer.addFeatures(features);

   	map.addLayer(vector_layer);
   	enabledStyle("styles");
}


function requestLayer(vectorlayer_id,map){
	var url = "/vector/geojson/" + vectorlayer_id
	var request = $.get(url);
	request.done(function(data){
		renderFeatureLayer(data,map);
	});
}


function init(options){
	var map_container = options["map_container"]
	var legend_container = options["legend_container"]
	var styles_container = options["styles_container"]	
	var vectorlayer_id = options["vectorlayer_id"]


	var map = initMap(map_container);
	requestLayer(vectorlayer_id,map);

}
