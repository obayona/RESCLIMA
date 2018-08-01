var BboxSelector = function(container){

	var vectors; // capa vectorial
	var box;
	var transform;

	var bbox = null;

	// se crean los elementgos graficos

	// el toolbox de opciones
	var menu_container = document.createElement("div");
	menu_container.style.backgroundColor = "#CEDBDA";
	menu_container.style.width = "500px";
	var instruction = document.createElement("div");
	instruction.innerHTML = "Dibuje un &aacute;rea";
	var newAreaBtn = document.createElement("input");
	newAreaBtn.type = "button";
  	newAreaBtn.value = unescape("Dibuje nueva %E1rea");
	newAreaBtn.style.display = 'none';
	newAreaBtn.addEventListener("click",function(event){
		dragNewBox();
	});
	menu_container.appendChild(instruction);
	menu_container.appendChild(newAreaBtn);

	var map_container = document.createElement("div");
	map_container.style.width = "500px";
	map_container.style.height = "300px";
	container.appendChild(menu_container);
	container.appendChild(map_container);
	
	// inicializacion del mapa
	var map = new OpenLayers.Map({
		div:map_container,
		projection:"EPSG:3857",
		displayProjection: new OpenLayers.Projection("EPSG:4326"),
		numZoomLevels:11,
		units: 'm'
	});
    var osm = new OpenLayers.Layer.OSM();
    vectors = new OpenLayers.Layer.Vector("Vector Layer");

    map.addLayers([osm,vectors]);


    box = new OpenLayers.Control.DrawFeature(vectors, OpenLayers.Handler.RegularPolygon, {
      handlerOptions: {
        sides: 4,
        snapAngle: 90,
        irregular: true,
        persist: true
      }
    });
    box.handler.callbacks.done = endDrag;
    map.addControl(box);

    transform = new OpenLayers.Control.TransformFeature(vectors, {
      rotate: false,
      irregular: true
    });
    transform.events.register("transformcomplete", transform, boxResize);
    map.addControl(transform);  
    map.addControl(box);
    box.activate();

    console.log("zoomToMaxExtent");
    map.zoomToMaxExtent();


	this.getBBox = function(){
		return bbox;
	}


	function endDrag(bbox) {
		var bounds = bbox.getBounds();
		setBounds(bounds);
		drawBox(bounds);
		box.deactivate();
		instruction.innerHTML = "Modifique el &aacute;rea o ...";
		newAreaBtn.style.display = "block";        
     }
      
    function dragNewBox() {
        box.activate();
        transform.deactivate();
        vectors.destroyFeatures();
        
        instruction.innerHTML = "Dibuje un &aacute;rea";
        newAreaBtn.style.display = 'none';
        
        setBounds(null); 
    }
      
	function boxResize(event) {
        setBounds(event.feature.geometry.bounds);
    }
      
    function drawBox(bounds) {
        var feature = new OpenLayers.Feature.Vector(bounds.toGeometry());
 
        vectors.addFeatures(feature);
        transform.setFeature(feature);
	}
      
    function setBounds(bounds) {
        if (bounds == null) {
          bbox = null;
        }
        else {
			b = bounds.clone().transform(map.getProjectionObject(), new OpenLayers.Projection("EPSG:4326"))
			bbox = {};
			bbox["minX"] = b.left;
			bbox["minY"] = b.bottom;    
			bbox["maxX"] = b.right;
			bbox["maxY"] = b.top;  
            
        }
    }


}