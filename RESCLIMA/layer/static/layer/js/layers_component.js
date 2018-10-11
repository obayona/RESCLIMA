Vue.component("layers_component",{
	template: `
		<!--Contenedor corredizo, se abre cuando open es true-->
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
					class="layerItem"
					v-bind:style="[shared.currentLayer.id==layer.id?{'background':'#EFEBE9'}:{}]">
						<div v-if="layer.state=='uninitialized'">
							<div style="width:100px;height:20px;margin:10px;" class="animated-background"></div>
							<div style="width:200px;height:20px;margin:10px;" class="animated-background"></div>
							<div style="width:20px;height:20px;margin:10px;" class="animated-background"></div>
						</div>
						<div v-if="layer.state!='uninitialized'">
							<h5 class="header layerTitle"
							 v-on:click.prevent="shared.currentLayer=layer">
								{{layer.title}}
							</h5>
							<p>{{layer.abstract}}</p>
							<h6>{{layer.data_date}}</h6>
							<div class="layerOptions" v-if="layer.state=='loaded'">
								<p class="range-field">
									<label>Transparencia</label>
									<input type="range" 
									min="0" 
									max="100" 
									value="0"
									v-model="layer.opacity"
									v-on:input="changeOpacity(layer)"/>
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
		/* Se lee el parametro "layers" del queryString
		del url, el cual tiene el siguiente formato:
		layers=id_capa1|id_capa2|...|id_capaN */
		var query_string = this.$route.query["layers"];
		if (!query_string){
			return;
		}
		// se obtienen los ids de las capas
		var layer_ids = query_string.split("|");
		// se crean objetos que representan las capas
		for(var i=0; i<layer_ids.length; i++){
			var id_layer = layer_ids[i];
			// Si el string es vacio, no se hace nada
			if(!id_layer){
				return;
			}
			var layer = {};
			layer["id"]=id_layer;
			layer["index"]=i;
			layer["state"]="uninitialized";
			layer["title"]="";
			layer["abstract"]="";
			layer["type"]="";
			layer["data_date"]="";
			layer["opacity"]=0;
			layer["styles"]=[];
			// se guarda el objeto en el store
			// compartido
			this.shared.layers.push(layer);
			// se piden los metadatos de la capa
			this.getLayerInfo(layer);
		}
		// se selecciona la capa actual (currentLayer)
		// es la primera capa
		if(layer_ids.length>0){
			var currentLayer = this.shared.layers[0];
			this.shared.currentLayer=currentLayer;
		}
	},
	data(){
		return {
			shared:store,
			open:true
		}
	},
	methods:{
		/*Metodo que realiza una peticion ajax
		para obtener los metadatos de la capa*/
		getLayerInfo(layer){
			var id_layer = layer["id"];
			var index = layer["index"];
			
			var url = "/layer/info/"+id_layer
			// referencia al componente
			var self = this;
			// peticion GET
			var request = $.get(url);
			request.done(function(data){
				layer["title"]=data["title"]
				layer["abstract"]=data["abstract"]
				layer["type"]=data["type"];
				layer["data_date"]=data["data_date"];
				layer["bbox"]=data["bbox"];
				// se actualiza el estado de la capa
				layer["state"]="metadata_loaded"
				// se agregan los estilos
				var styles = data["styles"]
				for(var i=0; i<styles.length; i++){
					var style = styles[i]
					// los estilos aun no tienen legenda
					// se agrega un array vacio
					style["legend"]=[];
					layer["styles"].push(style);
				}
				// se selecciona el primer estilo
				// como currentStyle de la capa
				if (layer["styles"].length>0){
					var style = layer["styles"][0];
					layer["currentStyle"]=style;
				}
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
		}
	}
})

