Vue.component("layers_component",{
	template: `
		<div>
			<div v-if="shared.results.length > 0">
				<div v-for="layer in shared.results">
					{{layer.title}}
				</div>
			</div>
			<div v-else>No hay resultados</div>
		</div>			
	`,
	data(){
		return {
			shared:model
		}
	}

})
