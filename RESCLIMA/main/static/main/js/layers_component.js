Vue.component("layers_component",{
	template: `
		<div>
			<!-- si el estado de las capas es searched se -->
			<!-- muestran los resultados -->
			<div v-if="state=='searched'">
				<div v-if="shared.layers.length > 0">
					<div>
						<a
						class="btn waves-effect waves-light gradient-45deg-light-blue-cyan" 
						v-bind:disabled="selected_count==0"
						v-on:click="visualizeLayers">
							<i class="material-icons left">remove_red_eye</i>Visualizar</a>
						<a
						class="btn waves-effect waves-light gradient-45deg-light-blue-cyan" 
						v-bind:disabled="selected_count==0"
						v-on:click="downloadLayers">
							<i class="material-icons left">file_download</i>Descargar</a>
					</div>
					<div v-for="layer in shared.layers">
						<div class="card">
							<div class="card-content">
								<span class="card-title">
									<input v-if="layer.selected" 
									type="checkbox"
									v-bind:id="layer.id"
									v-bind:value="layer.selected"
									v-on:input="selectLayer(layer)" checked >
									<input v-else
									type="checkbox"
									v-bind:id="layer.id"
									v-bind:value="layer.selected"
									v-on:input="selectLayer(layer)">
									<label v-bind:for="layer.id"></label>
									{{layer.title}}
								</span>
								<p>{{layer.abstract}}</p>
							</div>
						</div>		
					</div>
					<!-- Botones para visualizar y descargar-->
					<div v-if="shared.layers.length > 7">
						<a
						class="btn waves-effect waves-light gradient-45deg-light-blue-cyan" 
						v-bind:disabled="selected_count==0"
						v-on:click="visualizeLayers">
							<i class="material-icons left">remove_red_eye</i>Visualizar</a>
						<a
						class="btn waves-effect waves-light gradient-45deg-light-blue-cyan" 
						v-bind:disabled="selected_count==0"
						v-on:click="downloadLayers">
							<i class="material-icons left">file_download</i>Descargar</a>
					</div>
					<!-- botones de paginacion -->
					<div class="row"
						v-if="offset != 0 || offset < max_offset">
						<ul class="pagination">
							<li v-bind:class="{disabled: offset == 0}"
							    v-on:click.prevent="prev()">
								<a href="#!">
									<i class="material-icons">chevron_left</i>
								</a>
							</li>
							<li v-bind:class="{disabled: offset >= max_offset}"
							    v-on:click.prevent="next()">
								<a href="#!">
									<i class="material-icons">chevron_right</i>
								</a>
							</li>
						</ul>
					</div>
				</div>
				<div v-else>No hay resultados</div>
			</div>
			<!-- si el estado de las capas es loading se -->
			<!-- muestra una animacion -->
			<div v-if="state=='loading'" style="text-align: center;">			
				<div class="preloader-wrapper big active">
					<div class="spinner-layer spinner-blue-only">
						<div class="circle-clipper left">
							<div class="circle"></div>
						</div>
						<div class="gap-patch">
							<div class="circle"></div>
						</div>
						<div class="circle-clipper right">
							<div class="circle"></div>
						</div>
					</div>
				</div>
			</div>
			<!-- si el estado de las capas es fail se -->
			<!-- muestra un mensaje de error -->
			<div v-if="state=='fail'">
				<div class="red">
					<b>Ha ocurrido un error</b>
				</div>
			</div>
		</div>			
	`,
	data(){
		return {
			selected_count:0,
			state:'initial',
			// limit y offset controlan la paginacion
			limit:10,
			offset:0,
			// maximo offset, al principio
			// se tiene un valor negativo
			max_offset:-1,
			selected_layers : {},
			shared:store
		}
	},
	mounted(){
		this.$root.$on('searchLayers', this.restart);
	},
	methods:{
		restart(){
			this.state = "initial";
			this.limit = 10,
			this.offset = 0,
			this.max_offset = -1,
			this.selected_layers = {};
			this.searchLayers();
		},
		searchLayers(){
			console.log(this.selected_count)
			this.selected_count = Object.keys(this.selected_layers).length;
			// se obtienen los parametros de busqueda
			var data = this.shared.getPostData()
			if(data==null){
				return;
			}

			// referencia al componente
			var self = this;
			var url = "search/layers/";
			// se agrega el limit y el offset
			data["limit"] = self.limit;
			data["offset"] = self.offset;
			data["csrfmiddlewaretoken"] =  "{{csrf_token}}",
			headers = {'X-CSRFToken': this.shared.getCookie("csrftoken")}
			// se realiza la peticion ajax
			data = JSON.stringify(data);
			//var request = $.post(url,data,headers);
			self.state = "loading";	
			axios.post(url, data, {'headers':headers})
		    .then(response => {
		    	response = response['data'];
		    	var  results = response['layers'];
				// se determina el maximo offset
				var full_count = response["full_count"];
				var max_offset = full_count - self.limit;

				if(max_offset>0){
					self.max_offset = max_offset;
				}else{
					self.max_offset = 0;
				}

				// se copian los resultados en el
				// array layers
				var layers = self.shared.layers;
				console.log(self.selected_layers)
				console.log(layers)
				layers.splice(0, layers.length);

				for (var i=0;i< results.length; i++){
					layers.push(results[i]);
					if(results[i].id.toString() in self.selected_layers){
						results[i].selected = true;
					}
				}
				// se cambia el estado
				self.state = "searched";
		    })
		    .catch(e => {
		      self.state = "fail";
		    })
			
		},
		selectLayer(layer){
			
			layer.selected = !layer.selected;
			if(layer.selected==true) {
				this.selected_count +=1;
				this.selected_layers[layer.id.toString()] = layer.id; 
			}
			if(layer.selected==false){
				this.selected_count -=1;
				delete this.selected_layers[layer.id.toString()];
			}
		},
		visualizeLayers(){
			// abrea una nueva pestania para 
			// visualizar las capas
			var query_str = ""
			/*for(var i=0; i<this.shared.layers.length; i++){
				var layer = this.shared.layers[i];
				if (layer["selected"])
					query_str = query_str + String(layer["id"])+"|"
			}*/
			for (const [key, value] of Object.entries(this.selected_layers)) {
				console.log(key)
				console.log(value)
				query_str = query_str + key + "|"
			}
			query_str = query_str.slice(0, -1);

			var url = "layer/view/?layers="+query_str
			url = encodeURI(url)
			window.open(url,'_blank');
		},
		downloadLayers(){
			// se iteran todas las capas seleccionadas
			for(var i=0; i<this.shared.layers.length; i++){
				var layer = this.shared.layers[i];
				if (layer["selected"]){
					var url = "#"
					var link = document.createElement("a");
					link.style.display = 'none';
  					document.body.appendChild(link);
					link.setAttribute('download',"layer_"+layer["id"]);
					if(layer["type"]=="vector"){
						url = "/vector/export/"+layer["id"]
					}
					if(layer["type"]=="raster"){
						url = "/raster/export/"+layer["id"]	
					}
					link.href = url;
					link.click();
					document.body.removeChild(link);
				}
			}
		},
		prev(){
			if(this.offset <= 0){
				return;
			}
			this.offset -= this.limit;
			this.searchLayers();
		},
		next(){
			if(this.offset>=this.max_offset){
				return;
			}
			this.offset += this.limit;
			this.searchLayers();
		}
	}

})


