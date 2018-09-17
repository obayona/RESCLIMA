Vue.component("layers_component",{
	template: `
		<div>
			<div v-if="shared.layers.length > 0">
				<div>
					<button v-bind:disabled="selected_count==0">Visualizar</button>
					<button v-bind:disabled="selected_count==0">Descargar</button>
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
	`,
	data(){
		return {
			selected_count:0,
			shared:store
		}
	},
	methods:{
		selectLayer(layer){
			console.log("check layer",layer)
			layer.selected = !layer.selected;
			if(layer.selected==true) 
				this.selected_count +=1;
			if(layer.selected==false)
				this.selected_count -=1;
		}
	}

})
