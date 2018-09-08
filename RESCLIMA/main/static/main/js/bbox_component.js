

Vue.component("bbox_component",{
	template: `
		<div>
			<h4>Seleccione una regi&oacute;n</h4>
			<div id="container"></div>
		</div>
	`,
	mounted(){
		console.log(this.shared)
		bboxSelector = new BboxSelector("container",this.shared)
	},
	data(){
		return{
			bboxSelector: null,
			shared:model
		}
	}

})