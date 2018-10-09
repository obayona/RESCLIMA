Vue.component("layers_component",{
	template: `
		<div id="layerContainer"
		v-bind:style="[open?{'left':'0px'}:{'left':'-400px'}]">
			<div id="layerContainerOpen"
			class="gradient-45deg-light-blue-cyan"
			 v-on:click.prevent="open=!open">
				<i v-if="open" class="material-icons">keyboard_arrow_down</i>
				<i v-else class="material-icons">keyboard_arrow_up</i>
				Capas
				<i v-if="open" class="material-icons">keyboard_arrow_down</i>
				<i v-else class="material-icons">keyboard_arrow_up</i>
			</div>
			<div id="layerList" >
				<div v-if="shared.layers.length>0">
					<div v-for="layer in shared.layers"
					class="layerItem">
						<div v-if="layer.state=='uninitialized'">
							<div style="width:100px;height:20px;margin:10px;" class="animated-background"></div>
							<div style="width:200px;height:20px;margin:10px;" class="animated-background"></div>
							<div style="width:20px;height:20px;margin:10px;" class="animated-background"></div>
						</div>
						<div v-if="layer.state!='uninitialized'">
							<h5 class="header">{{layer.title}}</h5>
							<p>{{layer.abstract}}</p>
							<h6>{{layer.data_date}}</h6>
							<div class="layerOptions" v-if="layer.state=='loaded'">
								<p class="range-field">
									<label>Transparencia</label>
									<input type="range" min="0" max="100" value="0"/>
								</p>
								<div>
									<a style="padding:10px;color:green" href="#"><i class="material-icons">file_download</i>Descargar</a>
									<a style="padding:10px;color:red" href="#"><i class="material-icons">delete</i>Eliminar</a>
								</div>
							</div>
							<div v-else>
								<div class="animated-background" style="height:80px">Cargando...</div>
							</div>
						</div>
					</div>
				</div>
				<div v-else>
					<p>No hay capas</p>
				</div>
			</div>
		</div>
	`,
	mounted(){
		var query_string = this.$route.query["layers"];
		if (!query_string){
			return;
		}
		var layer_ids = query_string.split("|")
		for(var i=0; i<layer_ids.length; i++){
			var id_layer = layer_ids[i];
			if(!id_layer){
				return;
			}
			var layer = {};
			layer["id"]=id_layer;
			layer["state"]="uninitialized";
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
			shared:store,
			open:true
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
				layer["state"]="metadata_loaded"
				self.$root.$emit("layer_metadata",index)
			});
		}
	}
})

