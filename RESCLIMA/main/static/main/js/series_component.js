Vue.component("series_component",{
	// este componente debe reaccionar al arreglo de resultados
	// this.shared.series
	template: '<p>Resultados series de tiempo</p>',
	data(){
		return {
			shared: store // referencia al store de datos global
		}
	},
})
