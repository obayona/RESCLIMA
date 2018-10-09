var VectorLayer = function(map,id_layer,index){
	var layer = undefined;
	var url = "/vector/geojson/" + id_layer;

	function renderFeatureLayer(data){
		//var extent = getExtent(data.bbox);   	
		//map.zoomToExtent(extent);

		var geojson_format = new OpenLayers.Format.GeoJSON();

		layer = new OpenLayers.Layer.Vector(id_layer,{
			projection: new OpenLayers.Projection("EPSG:900913"),
			rendererOptions: {zIndexing: true}
		});

		var features = geojson_format.read(data);
		
		for (i=0; i<features.length; i++){
			feature = features[i];
			feature.geometry.transform('EPSG:4326','EPSG:900913');
		}
		layer.addFeatures(features);
		//callback({"id_layer":id_layer,"data":layer});
		map.addLayer(layer);
		// se obtiene el z-index de la capa
		var numLayers = store.layers.length;
		var zIndex = numLayers - index;
		layer.setZIndex(zIndex);
		// se actualiza el estado de la capa
		store.layers[index].state="loaded"
		console.log(index,zIndex)
		//enabledStyle("styles");
	}


	var request = $.get(url);
	request.done(function(data){
		renderFeatureLayer(data);
	});
}

var RasterLayer = function(map,id_layer,index){
	
	var layer = new OpenLayers.Layer.TMS(id_layer,
					"/tms/",
					{serviceVersion: "1.0",
					layername: id_layer,
					type: 'png',
					isBaseLayer: false,
					rendererOptions: {zIndexing: true}
				})
	layer.opacity = 0.7
	map.addLayer(layer);
	// se obtiene el z-index de la capa
	var numLayers = store.layers.length;
	var zIndex = numLayers - index;
	layer.setZIndex(zIndex);
	// se actualiza el estado de la capa
	store.layers[index].state="loaded"
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
		this.map = new OpenLayers.Map({
			div:"map_container",
			projection:"EPSG:3857",
			displayProjection: new OpenLayers.Projection("EPSG:4326"),
			numZoomLevels:11,
			units: 'm'
		});
		// control de zoom
		var pzb = new OpenLayers.Control.PanZoom({'position': new OpenLayers.Pixel(100,0) });
		pzb.position = new OpenLayers.Pixel(100,0);
		this.map.addControl(pzb);

		// se agrega una capa de OpenStreetMap
		var osm = new OpenLayers.Layer.OSM("OSM");
		this.map.addLayer(osm);
		// se la configura para que este al fondo
		osm.setZIndex(0);
		this.map.zoomToMaxExtent();
		
		// se reacciona al evento 
		// que se dispara cuando
		// se obtienen los metadatos de una capa
		this.$root.$on('layer_metadata', this.loadLayer);
	},
	data(){
		return {
			shared:store,
			map:null,
			layers:[]
		}
	},
	methods:{
		loadLayer(index){
			var layer = this.shared.layers[index];
			var self = this;
			if (layer["type"]=="vector"){
				VectorLayer(this.map,layer["id"],index);
			}
			if(layer["type"]=="raster"){
				RasterLayer(this.map,layer["id"],index);
			}
		}
	},
})

