// Objeto con funciones para 
// manipulacion de capas vectorial
var VectorLayer = function(map,shared,index){

	// Metodo para obtener los datos de una capa
	this.loadLayer=function(){
		// se recupera la capa
		// compartida
		var shared_layer = shared.layers[index];
		var id_layer = shared_layer["id"];
		// se realiza la peticion al servidor
		var url = "/vector/geojson/" + id_layer;
		var request = $.get(url);
		// TODO - implementar callbacks de error
		request.done(function(data){
			renderFeatureLayer(data);
		});
	}

	// Metodo que renderiza la capa
	function renderFeatureLayer(data){ 	
		var shared_layer = shared.layers[index];
		var id_layer = shared_layer["id"]

		//se obtiene el extent de la capa
		var extent = getExtent(shared_layer["bbox"]);
		// se guarda el extent
		shared_layer["extent"] = extent;

		// parser de geo_json
		var geojson_format = new OpenLayers.Format.GeoJSON();

		var layer = new OpenLayers.Layer.Vector(id_layer,{
			projection: new OpenLayers.Projection("EPSG:900913"),
			rendererOptions: {zIndexing: true}
		});
		// con el parser de geojson se obtienen los features
		// de la capa
		var features = geojson_format.read(data);
		// los features estan en EPSG:4326 
		// y deben ser transformados a EPSG:900913
		for (i=0; i<features.length; i++){
			feature = features[i];
			feature.geometry.transform('EPSG:4326','EPSG:900913');
		}
		// se agregan los features a la capa
		layer.addFeatures(features);
		// TODO - PENDIENTE CALLBACK DEL CLICK
		//callback({"id_layer":id_layer,"data":layer});
		
		// se agrega la capa al mapa
		map.addLayer(layer);
		// si el indice de la capa es 0
		// se realiza un zoom a su bbox
		if(index==0){
			map.zoomToExtent(extent);
		}

		/*
		Se obtiene el z-index de la capa.
		En OpenLayers el z-index define el 
		orden de las capas. Una capa con z-index = 0,
		sera la capa mas baja. Se quiere que las capas
		de shared.layers aparezcan de arriba hacia abajo,
		por eso hay que calcular el z-index
		*/
		var numLayers = shared.layers.length;
		var zIndex = numLayers - index;
		layer.setZIndex(zIndex);
		// se actualiza el estado de la capa
		var shared_layer = shared.layers[index];
		shared_layer["state"]="loaded";
		// se guarda una referencia a la capa
		// de OpenLayers
		shared_layer["openlayer_layer"]=layer;
		// se obtiene el estilo seleccionado
		// de la capa
		var selectedStyle = shared_layer["currentStyle"];
		if(selectedStyle){
			requestStyle(selectedStyle);
		}

	}

	// Metodo que obtiene el extent de la capa
	function getExtent(bbox_json){
		var geojson_format = new OpenLayers.Format.GeoJSON();
		var polygon = geojson_format.read(bbox_json)[0];
		polygon.geometry.transform('EPSG:4326','EPSG:900913');
		var coords = polygon.geometry.components[0]
		coords = coords.components
		var minX,minY,maxX,maxY
		minX = coords[0]["x"]
		minY = coords[0]["y"]
		maxX = coords[2]["x"]
		maxY = coords[2]["y"]
		return [minX,minY,maxX,maxY]
	}

	// Metodo para obtener el archivo SLD
	// que define el estilo
	function requestStyle(style){
		var style_id = style["id"]
		var url = "/vector/export_style/" + style_id;
		var request = $.get(url);
		request.done(function(sld){
			applyStyle(style,sld)
		})
	}

	// Metodo que aplica el estilo a la capa
	function applyStyle(layer_style,sld){
		var format = new OpenLayers.Format.SLD();
		var sld = format.read(sld);
		var namedLayers = sld.namedLayers;
		var namedLayer = null;
		for (var key in namedLayers) {
			if (namedLayers.hasOwnProperty(key)){
				namedLayer = namedLayers[key]
				break;
			}
		}

		var styles = namedLayer.userStyles;
		var style = styles[0];
		// se obtiene la capa
		var shared_layer = shared.layers[index];
		var layer = shared_layer["openlayer_layer"];
		layer.styleMap.styles["default"] = style;
		// se crea la leyenda
		createLegend(layer_style,style.rules);
		// se redibuja la capa
		layer.redraw();
	}

	// Este metodo recibe el objeto rules
	// lo transforma a un objeto mas simple
	// y lo guarda en el estilo seleccionado
	// del shared_layer
	function createLegend(layer_style,rules){
		var i = 0; 
		var length = rules.length;
		// se obtiene la capa compartida
		var legend = layer_style["legend"];
		// se recorren las reglas
		for (i;i<length;i++){
			var rule = rules[i];
			var value = rule.name;
			var symbolizer = rule.symbolizer;
			var color = getColor(symbolizer);
			legend.push({
				"color":color,
				"label":value,
			});
		}
	}

	// Este metodo recibe un objeto symbolizer
	// y retorna el color
	function getColor(symbolizer){
		var polygon = null;
		for (var key in symbolizer) {
			if (symbolizer.hasOwnProperty(key)){
				polygon = symbolizer[key]
				break;
			}
		}
		return polygon.fillColor;
	}

}

// Objeto con funciones para 
// manipulacion de capas raster
var RasterLayer = function(map,shared,index){
	
	// Metodo para obtener los datos de una capa
	this.loadLayer = function(){
		// capa compartida
		var shared_layer = shared.layers[index];
		var id_layer = shared_layer["id"]
		//se obtiene el extent de la capa
		var extent = getExtent(shared_layer["bbox"]);
		// se guarda el extent
		shared_layer["extent"] = extent;

		var layer = new OpenLayers.Layer.TMS(id_layer,
					"/tms/",
					{serviceVersion: "1.0",
					layername: id_layer,
					type: 'png',
					isBaseLayer: false,
					rendererOptions: {zIndexing: true}
				});
		//layer.opacity = 0.7
		map.addLayer(layer);

		// si el index es cero
		// se hace zoom a la capa
		if(index==0){
			map.zoomToExtent(extent);
		}
		/*
		Se obtiene el z-index de la capa.
		En OpenLayers el z-index define el 
		orden de las capas. Una capa con z-index = 0,
		sera la capa mas baja. Se quiere que las capas
		de shared.layers aparezcan de arriba hacia abajo,
		por eso hay que calcular el z-index
		*/
		var numLayers = store.layers.length;
		var zIndex = numLayers - index;
		layer.setZIndex(zIndex);
		// se actualiza el estado de la capa
		store.layers[index].state="loaded"

		// se guarda una referencia a la capa
		// de OpenLayers
		shared_layer["openlayer_layer"]=layer;
		// se obtiene el estilo seleccionado
		// de la capa
		var selectedStyle = shared_layer["currentStyle"];
		if(selectedStyle){
			requestStyle(selectedStyle);
		}
	}

	// Metodo que obtiene el extent de la capa
	function getExtent(bbox_json){
		var geojson_format = new OpenLayers.Format.GeoJSON();
		var polygon = geojson_format.read(bbox_json)[0];
		polygon.geometry.transform('EPSG:4326','EPSG:900913');
		var coords = polygon.geometry.components[0]
		coords = coords.components
		var minX,minY,maxX,maxY
		minX = coords[0]["x"]
		minY = coords[0]["y"]
		maxX = coords[2]["x"]
		maxY = coords[2]["y"]
		return [minX,minY,maxX,maxY]
	}

	// Metodo que carga informacion del estilo 
	// de la capa
	function requestStyle(style){
		var style_id = style["id"]
		/*var url = "/vector/export_style/" + style_id;
		var request = $.get(url);
		request.done(function(sld){
			applyStyle(style,sld)
		})*/
		console.log("se pide el estilo ****");
	}

}



Vue.component("map_component",{
	template: `
		<div id="map_component">
			<div id="map_container" style="width:100%;height: 700px;">
			</div>
		</div>
	`,
	mounted(){
		// se inicializa el mapa
		var map = new OpenLayers.Map({
			div:"map_container",
			projection:"EPSG:3857",
			displayProjection: new OpenLayers.Projection("EPSG:4326"),
			numZoomLevels:11,
			units: 'm'
		});

		// se agrega una capa de OpenStreetMap
		var osm = new OpenLayers.Layer.OSM("OSM");
		map.addLayer(osm);
		// se la configura para que este al fondo
		osm.setZIndex(0);
		map.zoomToMaxExtent();
		
		// se guarda la referencia del mapa
		this.shared.map = map;
		// se reacciona al evento 
		// que se dispara cuando
		// se obtienen los metadatos de una capa
		this.$root.$on('layer_metadata', this.loadLayer);
	},
	data(){
		return {
			shared:store
		}
	},
	methods:{
		loadLayer(index){
			var layer = this.shared.layers[index];
			var self = this;
			if (layer["type"]=="vector"){
				var vectorlayer = new VectorLayer(this.shared.map,this.shared,index);
				vectorlayer.loadLayer();
			}
			if(layer["type"]=="raster"){
				var rasterlayer = new RasterLayer(this.shared.map,this.shared,index);
				rasterlayer.loadLayer();
			}
		}
	},
})

