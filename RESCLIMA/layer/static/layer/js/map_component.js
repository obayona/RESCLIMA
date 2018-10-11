/*Objeto con funciones para 
manipulacion de capas vectorial
Recibe: el mapa de OpenLayers 
y la capa
*/

var VectorLayer = function(map,layer){

	// Metodo para obtener los datos de una capa
	this.loadLayer=function(){
		// se recupera la capa
		// compartida
		var id_layer = layer["id"];
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
		var id_layer = layer["id"]

		//se obtiene el extent de la capa
		var extent = getExtent(layer["bbox"]);
		// se guarda el extent
		layer["extent"] = extent;

		// parser de geo_json
		var geojson_format = new OpenLayers.Format.GeoJSON();

		// se crea una capa vectorial de OpenLayers
		// con proyeccion EPSG:900913
		var vectorlayer = new OpenLayers.Layer.Vector(id_layer,{
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
		vectorlayer.addFeatures(features);
		// TODO - PENDIENTE CALLBACK DEL CLICK
		//callback({"id_layer":id_layer,"data":layer});
		
		// se agrega la capa al mapa
		map.addLayer(vectorlayer);
		// si el indice de la capa es 0
		// se realiza un zoom a su bbox
		var index = layer["index"];
		if(index==0){
			map.zoomToExtent(extent);
		}

		// se configura el zIndex de la capa
		var zIndex = layer["zIndex"];
		vectorlayer.setZIndex(zIndex);
		// se actualiza el estado de la capa
		layer["state"]="loaded";
		// se guarda una referencia a la capa
		// de OpenLayers
		layer["openlayer_layer"]=vectorlayer;
		// se obtiene el estilo seleccionado
		// de la capa
		var selectedStyle = layer["currentStyle"];
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

	// Metodo Publico de requestStyle
	this.requestStyle = function(style){
		requestStyle(style);
	}

	// Metodo que aplica el estilo a la capa
	function applyStyle(layer_style,sld){
		// parser de sld
		var format = new OpenLayers.Format.SLD();
		// se obtiene un objeto con las reglas del estilo
		var sld = format.read(sld);
		// se obtiene la propiedad  namedLayer del
		// objeto sld
		var namedLayers = sld.namedLayers;
		var namedLayer = null;
		for (var key in namedLayers) {
			if (namedLayers.hasOwnProperty(key)){
				namedLayer = namedLayers[key]
				break;
			}
		}
		// se obtiene el estilo
		var styles = namedLayer.userStyles;
		var style = styles[0];
		var vectorlayer = layer["openlayer_layer"];
		// se aplica el estilo a la capa de OpenLayers
		vectorlayer.styleMap.styles["default"] = style;
		// se crea la leyenda
		createLegend(layer_style,style.rules);
		// se redibuja la capa
		vectorlayer.redraw();
	}

	// Este metodo recibe el objeto rules
	// lo transforma a un objeto mas simple
	// y lo guarda en el estilo seleccionado
	// del shared_layer
	function createLegend(layer_style,rules){
		var i = 0; 
		var length = rules.length;
		// se obtiene la leyenda
		var legend = layer_style["legend"];
		legend.splice(0,legend.length);
		// se recorren las reglas
		for (i;i<length;i++){
			var rule = rules[i];
			var value = rule.name;
			var symbolizer = rule.symbolizer;
			var color = getColor(symbolizer);
			// se guarda el color y el label
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

/*Objeto con funciones para 
manipulacion de capas raster
Recibe: el mapa de OpenLayers
y la capa
*/
var RasterLayer = function(map,layer){
	
	// Metodo para obtener los datos de una capa
	this.loadLayer = function(){
		// capa compartida
		var id_layer = layer["id"]
		//se obtiene el extent de la capa
		var extent = getExtent(layer["bbox"]);
		// se guarda el extent
		layer["extent"] = extent;
		// se crea una capa raster de OpenLayers
		var rasterlayer = new OpenLayers.Layer.TMS(id_layer,
					"/tms/",
					{serviceVersion: "1.0",
					layername: id_layer,
					type: 'png',
					isBaseLayer: false,
					rendererOptions: {zIndexing: true}
				});
		//layer.opacity = 0.7
		map.addLayer(rasterlayer);

		// si el index es cero
		// se hace zoom a la capa
		var index = layer["index"];
		if(index==0){
			map.zoomToExtent(extent);
		}
		// se configura el zIndex
		var zIndex = layer["zIndex"];
		rasterlayer.setZIndex(zIndex);
		// se actualiza el estado de la capa
		layer["state"]="loaded";

		// se guarda una referencia a la capa
		// de OpenLayers
		layer["openlayer_layer"]=rasterlayer;
		// se obtiene el estilo seleccionado
		// de la capa
		var selectedStyle = layer["currentStyle"];
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
		var url = "/raster/style_legend/" + style_id;
		var request = $.get(url);
		request.done(function(legend){
			createLegend(style,legend);
		})
	}

	function createLegend(layer_style,legend_json){
		var legend = layer_style["legend"];
		legend.splice(0,legend.length);

		for (i=0;i<legend_json.length;i++){
			var row = legend_json[i];
			// se guarda el color y el label
			legend.push(row);
		}

	}

	// Metodo Publico de requestStyle
	this.requestStyle = function(style){
		requestStyle(style);
	}

}


Vue.component("map_component",{
	template: `
		<div id="map_component">
			<!-- Contenedor del mapa de OpenLayers -->
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
		// se la configura para que esta sea la capa base
		osm.setZIndex(0);
		map.zoomToMaxExtent();
		
		// se guarda la referencia del mapa
		this.shared.map = map;
		// se reacciona al evento 
		// que se dispara cuando
		// se obtienen los metadatos de una capa
		this.$root.$on('layer_metadata', this.loadLayer);
		// se reacciona al evento
		// que se dispara cuando se cambia el estilo
		this.$root.$on("update_style",this.updateStyle);
	},
	data(){
		return {
			shared:store
		}
	},
	methods:{
		/*Metodo que se ejecuta cuando
		se actualizan los metadatos de la capa.
		Dependiendo del tipo de capa (vector,raster)
		se piden los datos y se las muestra en el mapa*/
		loadLayer(layer){
			// se guarda referencia al componente
			var self = this;
			var map = this.shared.map;
			/*Se calcula el zIndex de la capa.
			En OpenLayers el zIndex define la posicion
			de la capa. zIndex=0 es la capa base y asi 
			sucesivamente. Se quiere que la capa con index=0
			sea la capa mas superior, y asi en adelante, asi
			que se calcula el zIndex de la capa
			*/
			var numLayers = this.shared.layers.length;
			var index = layer["index"];
			var zIndex = numLayers - index;
			layer["zIndex"]=zIndex;
			if (layer["type"]=="vector"){
				// se crea un objeto con metodos para el manejo
				// de capas vectoriales
				var vectorlayer = new VectorLayer(map,layer);
				vectorlayer.loadLayer();
			}
			if(layer["type"]=="raster"){
				// se crea un objeto con metodos para el manejo
				// de capas raster
				var rasterlayer = new RasterLayer(map,layer);
				rasterlayer.loadLayer();
			}
		},
		updateStyle(){
			// se recupera la capa actual
			var currentLayer = this.shared.currentLayer;
			// se recupera el estilo de la capa actual
			var currentStyle = currentLayer.currentStyle;
			var map = this.shared.map;
			if(currentLayer["type"]=="vector"){
				var vectorlayer = new VectorLayer(map,currentLayer);
				vectorlayer.requestStyle(currentStyle);
			}
			if(currentLayer["type"]=="raster"){
				var rasterlayer = new RasterLayer(map,currentLayer);
				rasterlayer.requestStyle(currentStyle);
			}
		}
	},
})

