Vue.component("layers_component",{
	template: `
		<div id="layerList"
		v-bind:style="[open?{'left':'0px'}:{'left':'-220px'}]">
			<span><i class="material-icons">map</i>Capas</span>
			<div class="arrow" 
			 v-on:click.prevent="open=!open">
				<i v-if="open" class="material-icons">keyboard_arrow_left</i>
				<i v-else class="material-icons">keyboard_arrow_right</i>
			</div>
			<div>
				<div v-for="layer in shared.layers">
					<h5>{{layer.title}}</h5>
					<p>{{layer.abstract}}</p>
				</div>
			</div>
		</div>
	`,
	mounted(){
		var query_string = this.$route.query["layers"];
		var layer_ids = query_string.split("|")
		for(var i=0; i<layer_ids.length; i++){
			console.log(layer_ids[i],"recorro el url")
			var id_layer = layer_ids[i];
			var layer = {};
			layer["id"]=id_layer;
			layer["state"]="loading";
			layer["title"]="";
			layer["abstract"]="";
			layer["type"]="";
			layer["data_date"]="";
			this.shared.layers.push(layer);
			this.getLayerInfo(id_layer,i);
		}
	},
	data(){
		return {
			open:true,
			shared:store
		}
	},
	methods:{
		getLayerInfo(id_layer,index){
			var url = "/layer/info/"+id_layer
			var self = this;
			var request = $.get(url);
			request.done(function(data){
				var layer = self.shared.layers[index]
				layer["title"]=data["title"]
				layer["abstract"]=data["abstract"]
				layer["type"]=data["type"];
				layer["data_date"]=data["data_date"];
				self.$root.$emit("layer_metadata",index)
			});
		}
	}
})

