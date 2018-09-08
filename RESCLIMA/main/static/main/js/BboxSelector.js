var BboxSelector = function(container,model){

	console.log("el container id", container);
	var container = document.getElementById(container)
	console.log("El container",container)
	var vectors; // capa vectorial
	var box;
	var transform;

	// se crean los elementgos graficos

	// el toolbox de opciones
	var menu_container = document.createElement("div");
	menu_container.style.backgroundColor = "#CEDBDA";
	menu_container.style.width = "500px";
	menu_container.style.zIndex = "1";
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
	map_container.style.zIndex = "-1";
	console.log("aqui se cae")
	container.appendChild(menu_container);
	container.appendChild(map_container);
	container.style.zIndex = "2";
	

	// inicializacion del mapa
	var map = new OpenLayers.Map({
		div:map_container,
		projection:"EPSG:3857",
		displayProjection: new OpenLayers.Projection("EPSG:4326"),
		numZoomLevels:11,
		units: 'm'
	});
    var osm = new OpenLayers.Layer.OSM();
    var StyleMap = new OpenLayers.StyleMap({
                    // a nice style for the transformation box
                    "transform": new OpenLayers.Style({
			                        display: "${getDisplay}",
			                        cursor: "${role}",
			                        pointRadius: 5,
			                        fillColor: "white",
			                        fillOpacity: 1,
			                        strokeColor: "black"
                  				 })
                	});
    vectors = new OpenLayers.Layer.Vector("Vector Layer", {
    	styleMap: StyleMap
    });

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
    console.log(box.handler.callbacks);
    map.addControl(box);

    transform = new OpenLayers.Control.TransformFeature(vectors, {
      renderIntent:"transform",
      rotate: false,
      irregular: true
    });
    transform.events.register("transformcomplete", transform, boxResize);
    map.addControl(transform);  
    map.addControl(box);
    box.activate();

    map.zoomToMaxExtent();



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
		feature.style = {fillColor: "#9FBFDC",
						 fillOpacity: 0.5};
        vectors.addFeatures(feature);
        transform.setFeature(feature);
	}
      
    function setBounds(bounds) {
        if (bounds == null) {
          model.bbox = null;
        }
        else {
			b = bounds.clone().transform(map.getProjectionObject(), new OpenLayers.Projection("EPSG:4326"))
			bbox = {};
			bbox["minX"] = b.left;
			bbox["minY"] = b.bottom;    
			bbox["maxX"] = b.right;
			bbox["maxY"] = b.top; 
			model.bbox = bbox 
            
        }
    }
}
