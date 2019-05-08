
function rainbow(numOfSteps, step) {
    // This function generates vibrant, "evenly spaced" colours (i.e. no clustering). This is ideal for creating easily distinguishable vibrant markers in Google Maps and other apps.
    // Adam Cole, 2011-Sept-14
    // HSV to RBG adapted from: http://mjijackson.com/2008/02/rgb-to-hsl-and-rgb-to-hsv-color-model-conversion-algorithms-in-javascript
    var r, g, b;
    var h = step / numOfSteps;
    var i = ~~(h * 6);
    var f = h * 6 - i;
    var q = 1 - f;
    switch(i % 6){
        case 0: r = 1; g = f; b = 0; break;
        case 1: r = q; g = 1; b = 0; break;
        case 2: r = 0; g = 1; b = f; break;
        case 3: r = 0; g = q; b = 1; break;
        case 4: r = f; g = 0; b = 1; break;
        case 5: r = 1; g = 0; b = q; break;
    }
    var c = "#" + ("00" + (~ ~(r * 255)).toString(16)).slice(-2) + ("00" + (~ ~(g * 255)).toString(16)).slice(-2) + ("00" + (~ ~(b * 255)).toString(16)).slice(-2);
    return (c);
}

/**Funcion que recibe un layer component y datos de longitud
 * y latitud y grafica un punto segun cada lectura y finalmente
 * las grafica el la capa y agrega la capa al mapa
 * el formato de los datos para graficar el viaje es un archivo .gpx
 * retorna una capa vectorial
 */
function drawTravelGPX(map, location_file_gpx){
    var colors = ['#fb3308', '#7f8c3b', '#5c462e', '#474dcc', '#e1399f', '#a1e139', '#398ae1', '#e17139', '#b40a26', '#0ab4b4', '#b4710a', '#0ab486']
	color = colors[Math.random() * colors.length | 0]

    var lgpx = new OpenLayers.Layer.Vector("Lakeside cycle ride", {
        strategies: [new OpenLayers.Strategy.Fixed()],
        protocol: new OpenLayers.Protocol.HTTP({
            url: location_file_gpx,
            format: new OpenLayers.Format.GPX()
        }),
        style: {strokeColor: color, strokeWidth: 5, strokeOpacity: 0.5},
        projection: new OpenLayers.Projection("EPSG:4326")
	});
	
    // se agrega la capa al mapa
	map.addLayer(lgpx);
	return lgpx
}

function setMapCenter(loc_metadata, map,sensor){
	var url = loc_metadata.replace("gpxfile","metadata");
	var zoom = 15;
	var request = $.get(url);
	var bbox = '';

	$.ajax({
		type: 'get',
		async: false,
		url: url,
		data: '',
		success: function(data) {
			setBbox(sensor,data.bbox)
			var lon = data.lon;
			var lat = data.lat;
			var lonLat = new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());
			sensor['lonlat'] = lonLat;
			map.setCenter(lonLat, zoom);
		}
	  });	  
	//request.done(function(data){

	//});
}

function setBbox(sensor, bbox){
	sensor['bbox'] = bbox;
}

Vue.component("tracking_component",{
	template: `
		<!--Contenedor corredizo, se abre cuando open es True-->
		<div id="layerContainer"
		v-bind:style="[open?{'left':'0px'}:{'left':'-400px'}]">
			
			<!-- Boton que abre y cierra el contenedor-->
			<div id="layerContainerOpen"
			class="gradient-45deg-light-blue-cyan"
			 v-on:click.prevent="open=!open">
				<!-- Dependiendo del valor de open se muestra un icono diferente-->
				<i v-if="open" class="material-icons">keyboard_arrow_down</i>
				<i v-else class="material-icons">keyboard_arrow_up</i>
				Capas
				<!-- Dependiendo del valor de open se muestra un icono diferente-->
				<i v-if="open" class="material-icons">keyboard_arrow_down</i>
				<i v-else class="material-icons">keyboard_arrow_up</i>
			</div>
			<!-- Wrapper-->
			<div class="boxWrapper">
				<!-- Menu con opciones de los sensores-->
				<div class="positionMenu">
					<div class="positionBtn"
					 v-on:click.prevent="moveLayer(-1)">
						<i class="material-icons">keyboard_arrow_up</i>
					</div>
					<div class="positionBtn"
					 v-on:click.prevent="moveLayer(1)">
						<i class="material-icons">keyboard_arrow_down</i>
					</div>
				</div>
				<!-- Contenedor con la lista de capas -->
				<div id="layerList" >
					<!-- Si hay capas en shared.layers se muestra la lista-->
					<div v-if="shared.sensors.length>0">
						<!-- Contenedor de la capa -->
						<!-- se intera sobre el array shared.layers -->
						<!-- Si la capa es igual a currentLayer, se pinta-->
						<div v-for="sensor in shared.sensors"
						class="layerItem"
						v-bind:style="[shared.currentSensor.id==sensor.id?{'background':'#EFEBE9','border-width': '3px'}:{}]">
							<!-- Si la capa tiene estado uninitialized-->
							<!-- Se muestran animaciones-->
							<div v-if="sensor.state=='uninitialized'">
								<div style="width:100px;height:20px;margin:10px;" class="animated-background"></div>
								<div style="width:200px;height:20px;margin:10px;" class="animated-background"></div>
								<div style="width:20px;height:20px;margin:10px;" class="animated-background"></div>
							</div>
							<!-- Si la capa tiene estado distinto a uninitialized-->
							<!-- Se muestran los metadatos de la capa -->
							<div v-if="sensor.state!='uninitialized'">
								<!-- Opcion zoom a la capa-->
								<div style="height:100%;position: relative;">
									<div style="position:absolute;right:10px;">
										<span title="Zoom a la capa"
										  class="layerBtn"
										  v-on:click.prevent="zoomToLayer(sensor)">
											<i class="material-icons">zoom_in</i>
										</span>
										
									</div>
								</div>
								<!-- El titulo de la capa-->
								<!-- Si se da click es esta capa, se convierte en-->
								<!-- currentLayer -->
								<h5 class="header layerTitle"
								 v-on:click.prevent="shared.currentSensor=sensor">
									{{sensor.name}}
								</h5>
								<!-- El resumen de la capa -->
								<p>{{sensor.description}}</p>
								<!-- La fecha de la toma de datos del sensor-->
								<h6>{{sensor.data_date}}</h6>
								<!--TimePicker para cambiar la forma como se grafican los puntos -->
								<div class="row">
									<div id="init_date" class="col s6">
									<input class="col s12" type='date'></input>
										<p class="col s6 range-field">
											<label>Horas</label>
											<input type="range" 
											min="0" 
											max="24" 
											value="0"
											v-on:input=""/>
										</p>
										<p class="col s6 range-field">
											<label>Minutos</label>
											<input type="range" 
											min="0" 
											max="60" 
											value="0"
											v-on:input=""/>
										</p>
									</div>	
									<div id="last_date" class="col s6">
									<input class="col s12" type='date'></input>
										<p class="col s6 range-field">
											<label>Horas</label>
											<input type="range" 
											min="0" 
											max="24" 
											value="0"
											v-on:input=""/>
										</p>
										<p class="col s6 range-field">
											<label>Minutos</label>
											<input type="range" 
											min="0" 
											max="60" 
											value="0"
											v-on:input=""/>
										</p>
									</div>		
									<button 
									v-on:click="changeDate(sensor)">Actualizar</button>							
								</div>
								<!-- Contenedor con opciones de la capa -->
								<!-- Solo se muestra si el estado de la capa es loaded-->
								<div class="layerOptions" v-if="sensor.state=='loaded'">
									<!-- Slider para controlar la transparencia-->
									<p class="range-field">
										<label>Transparencia</label>
										<input type="range" 
										min="0" 
										max="100" 
										value="0"
										v-model="sensor.opacity"
										v-on:input="changeOpacity(sensor)"/>
									</p>
									<!-- Links para remover el sensor-->
									<div>
										<a style="padding:10px;color:red" href="#!" v-on:click.prevent="removeLayer(sensor)">
											<i class="material-icons">delete</i>Eliminar
										</a>
									</div>
								</div>
								<!-- Si la capa no tiene estado loaded-->
								<!-- no se muestran las opciones de la capa,-->
								<!-- se muestra una animacion-->
								<div v-else>
									<div class="animated-background" style="height:80px">Cargando...</div>
								</div>
							</div>
						</div>
					</div>
					<!-- Si no hay capas en shared.sensors se muestra un mensaje-->
					<div v-else>
						<p>No hay sensores</p>
					</div>
				</div>
			</div>
		</div>
	`,
	mounted(){
		/*Se posiciona correctamente el elemento*/
		var layerContainer = document.getElementById('layerContainer')
		var elements = document.getElementsByClassName("navbar-fixed");
		var navbar = elements[0];
		var height = navbar.getBoundingClientRect()["height"];
		height = Math.ceil(height);
		layerContainer.style.top = String(height) + "px";

		/* Se lee el parametro "layers" del queryString
		del url, el cual tiene el siguiente formato:
		sensors=id_sensor1|id_sensor2|...|id_sensorN */
		var query_string = this.$route.query["sensors"];
		var init_date = (query_string.split("/")[1].split("=")[1])
		var end_date  = (query_string.split("/")[2].split("=")[1])
		if (!query_string){
			return;
		}
		var sensors = query_string.split("/")[0];
		var path_to_gpx = '/trackfiles/gpxfile/'
		// se obtienen los ids de las capas
		var sensor_ids = sensors.split("|");
		// se crean objetos que representan las capas
		for(var i=0; i<sensor_ids.length; i++){
			var id_sensor = sensor_ids[i];
			var location_file_gpx = path_to_gpx+id_sensor+"/"+init_date+"/"+end_date+"/"
			// Si el string es vacio, no se hace nada
			if(!id_sensor){
				return;
			}
			var sensor = {};
			sensor["id"]=id_sensor;
			sensor["index"]=i;
			sensor["state"]="uninitialized";
			sensor["name"] = "";
			sensor["description"]="";
			sensor["data_date"]="";
			sensor["opacity"]=0;
			// se guarda el objeto en el store
			// compartido
			this.shared.sensors.push(sensor);
			this.shared.layers.push(sensor)
			// se piden los metadatos de la capa
			this.getSensorLayerInfo(sensor);
			sensor["openlayer_layer"] = drawTravelGPX(this.shared.map, location_file_gpx);
			sensor["state"] = "loaded";
			setMapCenter(location_file_gpx,this.shared.map, sensor)
			var extent = getExtent(sensor["bbox"]);
			console.log(extent)
			// se guarda el extent
			sensor["extent"] = extent;
		}
		// se selecciona la capa actual (currentLayer)
		// es la primera capa
		if(sensor_ids.length>0){
			var currentLayer = this.shared.layers[0];
			var currentSensor = this.shared.sensors[0]
			this.shared.currentLayer=currentLayer;
			this.shared.currentSensor = currentSensor
		}
	},
	data(){
		return {
			shared:store,
			open:true,
		}
	},
	methods:{
		/*Metodo que realiza una peticion ajax
		para obtener los metadatos de la capa*/
		getSensorLayerInfo(layer){
			var id_sensor = layer["id"]
			var index = layer["index"];
			
			var url = "/trackfiles/trackpoints/info/"+id_sensor
			// referencia al componente
			var self = this;
			// peticion GET
			var request = $.get(url);
			request.done(function(data){
				layer["title"]=data["title"]
				layer["description"]=data["description"]
				layer["data_date"]=data["data_date"];
				layer["name"]= data["name"]
				// se actualiza el estado de la capa
				if(layer["state"]!=="loaded"){
					layer["state"]="metadata_loaded"
				}
				// se agregan los estilos
				// se notifica a los otros componentes
				// que la capa ya tiene metadatos
				self.$root.$emit("layer_metadata",layer);
			});
		},
		/*
		Metodo para actualizar la transparencia
		de una capa
		*/
		changeOpacity(layer){
			var opacity = layer["opacity"];
			var openlayer_layer = layer["openlayer_layer"];
			openlayer_layer.setOpacity(1-opacity/100);
		},
		/*
		Metodo para cambiar la ruta de un sensor
		segun la fecha
		*/
		changeDate(sensor){
			console.log(event.srcElement)
		},
		/*
		Metodo para realizar un zoom a la capa
		*/
		zoomToLayer(layer){
			var extent = layer["extent"];
			if(extent){
				var map = this.shared.map;
				map.setCenter(layer['lonlat'],15)
			}
		},
		moveLayer(direction){
			var layers = this.shared.sensor;
			var currentLayer = this.shared.currentSensor;
			var ini = currentLayer["index"];
			var end = ini + direction;
			var limit = layers.length - 1;
			if(end<0 || end > limit ){
				return;
			}
			layers.splice(ini,1);
			layers.splice(end,0,currentLayer);
			// actualizar los index
			currentLayer["index"]=end;
			currentLayer["openlayer_layer"]
			var changedLayer = layers[ini];
			changedLayer["index"]=ini;
			// actualizar los zIndex
			var zIndex1 = currentLayer["openlayer_layer"].getZIndex()
			var zIndex2 = changedLayer["openlayer_layer"].getZIndex()
			currentLayer["openlayer_layer"].setZIndex(zIndex2);
			changedLayer["openlayer_layer"].setZIndex(zIndex1);

		},
		openFilters(layer){
			this.$root.$emit("openFilters",layer);
		},
		removeLayer(removing_layer){
			var index = removing_layer.index;
			var layers = this.shared.sensors;
			// se elimina la capa de la lista 
			// de capas
			layers.splice(index,1);

			var numLayers = layers.length;

			// se actualizan los index y z-index
			// de las otras capas
			for(var i=0;i<numLayers;i++){
				var layer = layers[i];
				layer.index = i;
				layer.zIndex = numLayers - index;
				layer.openlayer_layer.setZIndex(layer.zIndex)
			}
			// se remueve el capa del mapa de openlayers
			var map = this.shared.map;
			map.removeLayer(removing_layer.openlayer_layer,false);
			removing_layer.openlayer_layer.destroy();

			if(layers.length>0){
				this.shared.currentSensor = layers[0];
				this.shared.currentLayer = layers[0];
			}else{
				this.shared.currentSensor = null;
				this.shared.currentLayer = null;
			}
		}
	}
})
