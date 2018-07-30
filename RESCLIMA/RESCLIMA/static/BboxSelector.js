var BboxSelector = function(container){

	var vectors; // capa vectorial
	//banderas
	var flagDraw = false;
	var flagDown = false;

	var bbox;
	var p0,pf;

	// se crean los elementgos graficos

	// el toolbox de opciones
	var toolbox_container = document.createElement("div");
	toolbox_container.style.backgroundColor = "#CEDBDA";
	toolbox_container.style.width = "500px";
	var drawBtn = document.createElement("img");
	drawBtn.src = "/static/IconDraw.png";
	drawBtn.style.width = "30px";
	drawBtn.style.height = "30px";


	drawBtn.addEventListener("click",function(e){
		flagDraw = !flagDraw;
		if(flagDraw){
			drawBtn.style.backgroundColor = "#A19F9F";
		}
		else{
			drawBtn.style.backgroundColor = "";
			map.setOptions({restrictedExtent: null});
		}
	});

	toolbox_container.appendChild(drawBtn);
	container.appendChild(toolbox_container);

	var map_container = document.createElement("div");
	map_container.style.width = "500px";
	map_container.style.height = "300px";
	container.appendChild(map_container);

	// se inicializa el mapa
	var map = new OpenLayers.Map({
		div:map_container,
		projection:"EPSG:3857",
		displayProjection: new OpenLayers.Projection("EPSG:4326"),
		numZoomLevels:11,
		units: 'm'
	});
	// se crea una capa de open street map
	var osm = new OpenLayers.Layer.OSM("OSM");


	// se crea una capa vectorial para dibujar
	var renderer = OpenLayers.Util.getParameters(window.location.href).renderer;
  	renderer = (renderer) ? [renderer] : OpenLayers.Layer.Vector.prototype.renderers;
    
    vectors = new OpenLayers.Layer.Vector("Vector Layer", {
        renderers: renderer
    });

    // se agregan las capas
    map.addLayers([osm,vectors]);
    // se muestra el mapa
	map.zoomToMaxExtent();
    
    // se desactiva el drag
    var extent = map.getExtent();
    map.setOptions({restrictedExtent: extent});


	// se configuran los eventos
	map.events.register("mousedown", map, function (e) {
		flagDown = true;            
		var point = map.getLonLatFromPixel( this.events.getMousePosition(e) )     
	    // se guarda el punto inicial
	    if(flagDraw){
	    	p0 = point;
	    	// se desactiva el drag
    		var extent = map.getExtent();
    		map.setOptions({restrictedExtent: extent});	
	    }
	},true);

	map.events.register("mousemove", map, function (e) {            
		var point = map.getLonLatFromPixel(this.events.getMousePosition(e))      
	    if(flagDraw && flagDown){
	    	pf = point;
	    	vectors.removeAllFeatures();
	    	bbox = createPolygon();
	    	vectors.addFeatures(bbox);
			vectors.redraw();
	    	return;
	    }
	 
	});

	map.events.register("mouseup", map, function (e) {            
	var point = map.getLonLatFromPixel( this.events.getMousePosition(e) )
		flagDraw = false;
		drawBtn.style.backgroundColor = "";
		map.setOptions({restrictedExtent: null});
	    flagDown=false;
	    p0 = undefined;
	    pf = undefined;
	});


	var createPolygon = function(){
		var point1 = new OpenLayers.Geometry.Point(p0.lon,p0.lat);
		var point2 = new OpenLayers.Geometry.Point(pf.lon,p0.lat);
		var point3 = new OpenLayers.Geometry.Point(pf.lon,pf.lat);
		var point4 = new OpenLayers.Geometry.Point(p0.lon, pf.lat);
		
		var points = [point1,point2,point3,point4,point1];
		var linearRing = new OpenLayers.Geometry.LinearRing(points);
		var polygonFeature = new OpenLayers.Feature.Vector(
                new OpenLayers.Geometry.Polygon([linearRing]));
		polygonFeature.style = {strokeColor: "#F07C1B",
								fillColor: "#9FBFDC",
								fillOpacity: 0.5}

		return polygonFeature;
	}


	this.getBBox = function(){
		if(!bbox){
			return null;	
		}
		var copy_bbox = bbox.clone();
		copy_bbox.geometry.transform('EPSG:900913','EPSG:4326');
		copy_bbox.geometry.calculateBounds();
		var bounds = copy_bbox.geometry.bounds; 
		var box = {};
		box["minX"]=bounds["left"];
		box["maxX"]=bounds["right"];
		box["minY"]=bounds["bottom"];
		box["maxY"]=bounds["top"];
		return box;
		
	}


}