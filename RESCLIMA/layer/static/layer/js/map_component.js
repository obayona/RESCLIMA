var VectorLayer = function(map,id_layer){
	var layer = undefined;
	var url = "/vector/geojson/" + id_layer;

	function renderFeatureLayer(data){
		//var extent = getExtent(data.bbox);   	
		//map.zoomToExtent(extent);

		var geojson_format = new OpenLayers.Format.GeoJSON();

		layer = new OpenLayers.Layer.Vector(id_layer,{
			projection: new OpenLayers.Projection("EPSG:900913")
		});

		var features = geojson_format.read(data);
		
		for (i=0; i<features.length; i++){
			feature = features[i];
			feature.geometry.transform('EPSG:4326','EPSG:900913');
		}
		layer.addFeatures(features);
		//callback({"id_layer":id_layer,"data":layer});
		map.addLayer(layer);
		//enabledStyle("styles");
	}


	var request = $.get(url);
	request.done(function(data){
		renderFeatureLayer(data);
	});
}



Vue.component("map_component",{
	template: `
		<div id="map_component">
			<div id="map_container" style="width:100%;height: 700px;">
			</div>
		</div>
	`,
	mounted(){
		this.map = new OpenLayers.Map({
			div:"map_container",
			projection:"EPSG:3857",
			displayProjection: new OpenLayers.Projection("EPSG:4326"),
			numZoomLevels:11,
			units: 'm'
		});
		var osm = new OpenLayers.Layer.OSM("OSM");
		this.map.addLayer(osm);
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
			console.log("mensaje recibido")
			var layer = this.shared.layers[index];
			var self = this;
			if (layer["type"]=="vector"){
				console.log("ceando la capa")
				VectorLayer(this.map,layer["id"]);
			}
		}
	},
})

