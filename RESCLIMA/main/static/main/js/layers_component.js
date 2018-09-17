Vue.component("layers_component",{
	template: `
		<div>
			<div v-if="shared.results.length > 0">
				<div>
					<button>Visualizar</button>
					<button>Descargar</button>
				</div>
				<div v-for="layer in shared.results">
					<div class="card">
						<div class="card-content">
							<span class="card-title">
								<input type="checkbox" v-bind:id="layer.id" v-model="layer.selected">
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
			shared:store
		}
	}

})
