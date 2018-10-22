Vue.component("layers_component",{
	template: `
		<div>
			<!-- si el estado de las capas es searched se -->
			<!-- muestran los resultados -->
			<div v-if="shared.layers_state=='searched'">
				<div v-if="shared.layers.length > 0">
					<div>
						<a
						class="btn waves-effect waves-light gradient-45deg-light-blue-cyan" 
						v-bind:disabled="selected_count==0"
						v-on:click="visualizeLayers">
							<i class="material-icons left">remove_red_eye</i>Visualizar</a>
						<a
						class="btn waves-effect waves-light gradient-45deg-light-blue-cyan" 
						v-bind:disabled="selected_count==0">
							<i class="material-icons left">file_download</i>Descargar</a>
					</div>
					<div v-for="layer in shared.layers">
						<div class="card">
							<div class="card-content">
								<span class="card-title">
									<input
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
				</div>
				<div v-else>No hay resultados</div>
			</div>
			<!-- si el estado de las capas es loading se -->
			<!-- muestra una animacion -->
			<div v-if="shared.layers_state=='loading'">
				<div v-if="shared.state=='loading'">
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
			</div>
			<!-- si el estado de las capas es fail se -->
			<!-- muestra un mensaje de error -->
			<div v-if="shared.layers_state=='fail'">
				<div class="red">
					<b>Ha ocurrido un error</b>
				</div>
			</div>
		</div>			
	`,
	data(){
		return {
			selected_count:0,
			shared:store
		}
	},
	methods:{
		selectLayer(layer){
			layer.selected = !layer.selected;
			if(layer.selected==true) 
				this.selected_count +=1;
			if(layer.selected==false)
				this.selected_count -=1;
		},
		visualizeLayers(){
			// open a new window to visualize the layers
			var query_str = ""
			for(var i=0; i<this.shared.layers.length; i++){
				var layer = this.shared.layers[i];
				if (layer["selected"])
					query_str = query_str + String(layer["id"])+"|"
			}
			query_str = query_str.slice(0, -1);

			var url = "layer/view/?layers="+query_str
			url = encodeURI(url)
			window.open(url,'_blank');
		}
	}

})


