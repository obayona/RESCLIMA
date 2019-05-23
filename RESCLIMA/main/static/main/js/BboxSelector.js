var BboxSelector = function(container,callback){

	var container = document.getElementById(container)
	var vectors; // capa vectorial
	var box;
	var transform;

	// se crean los elementgos graficos

	// el toolbox de opciones
	var menu_container = document.createElement("div");
	menu_container.style.backgroundColor = "#CEDBDA";
	menu_container.style.width = "700px";
	menu_container.style.display="inline-block";
	menu_container.style.zIndex = "1";
	menu_container.style.padding = "10px";

	var instruction = document.createElement("div");
	instruction.style.display = "inline-block";
	instruction.innerHTML = "Dibuje un &aacute;rea";
	var newAreaBtn = document.createElement("input");
	newAreaBtn.type = "button";
	newAreaBtn.className = "ml-2"
	newAreaBtn.value = unescape("Dibuje nueva %E1rea");
	newAreaBtn.style.display = 'none';
	newAreaBtn.addEventListener("click",function(event){
		dragNewBox();
	});
	menu_container.appendChild(instruction);
	menu_container.appendChild(newAreaBtn);

	var icon = document.createElement("i")
	icon.className ="material-icons"
	icon.innerHTML ="add_location"

	var newLocatPosBtn = document.createElement("a");
	//newLocatPosBtn.type = "button";
	newLocatPosBtn.id = "bboxButton";
	newLocatPosBtn.value = unescape("aquí");
	newLocatPosBtn.className ="right btn-floating  pink lighten-4";
	newLocatPosBtn.setAttribute("data-toggle","tooltip");
	newLocatPosBtn.setAttribute("title","mi ubicación");
	newLocatPosBtn.addEventListener("click",function(event){
		handlePermission();
	});
	newLocatPosBtn.appendChild(icon)
	menu_container.appendChild(newLocatPosBtn);

	var map_container = document.createElement("div");
	map_container.style.width = "700px";
	map_container.style.display="inline-block";
	map_container.style.height = "300px";
	map_container.style.zIndex = "-1";
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


	this.setBBox = function(left,bottom, rigth, top){
		var bounds = new OpenLayers.Bounds(left,bottom, rigth, top);
		bounds = bounds.transform(new OpenLayers.Projection("EPSG:4326"),map.getProjectionObject())
		drawBox(bounds);
		box.deactivate();
		instruction.innerHTML = "Modifique el &aacute;rea o ...";
		newAreaBtn.style.display = "inline-block";   
	}

	function endDrag(bbox) {
		var bounds = bbox.getBounds();
		setBounds(bounds);
		drawBox(bounds);
		box.deactivate();
		instruction.innerHTML = "Modifique el &aacute;rea o ...";
		newAreaBtn.style.display = "inline-block";        
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
			callback(null)
		}
		else {
			b = bounds.clone().transform(map.getProjectionObject(), new OpenLayers.Projection("EPSG:4326"))
			callback(b)
		}
	}

	var geoSettings = {
		enableHighAccuracy: true,
		timeout: 5000,
		maximumAge: 0
	};

	function setInitLocation(position){
		var crds = position.coords;
		var zoom = 10;
		var lonLat = new OpenLayers.LonLat(crds.longitude,crds.latitude).transform(
			new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());
		map.setCenter(lonLat, zoom);
	}
	function error(err) {
		console.warn('ERROR(' + err.code + '): ' + err.message);
	  };

	function handlePermission() {
		navigator.permissions.query({name:'geolocation'}).then(function(result) {
		if (result.state == 'prompt' || result.state == 'granted' ) {
			var position = navigator.geolocation.getCurrentPosition(setInitLocation,error,geoSettings);
		  } else if (result.state == 'denied') {
			geoBtn.style.display = 'inline';
		  }
		});
	}
}

