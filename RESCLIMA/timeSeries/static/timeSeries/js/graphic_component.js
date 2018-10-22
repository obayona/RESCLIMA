
Vue.component("graphic_component",{
	template: `
		<div id="graphic_component">
			<!-- Contenedor de la grafica de serie de tiempo en Plotly -->
		</div>
	`,
	mounted(){
		var self = this;
		this.$root.$on('serie_metadata', this.plotSingleTrace);
	},

	data(){
		return {
			shared:store
		}
	},

	methods:{
		//method that draws a plotly graphic with the values of a serie object
		plotSingleTrace(serie){
			var TESTER = document.querySelectorAll("[data-plot-id=\'"+serie["variable_id"]+"\']")[0];
			console.log(TESTER);
			var data = []
			var x_len = serie["x_values"].length;
			var y_len = serie["y_values"].length;
			var x_values_list = serie["x_values"];
			var y_values_list = serie["y_values"];

			if(x_len!=y_len){
				console.log("Unequal lengths");
				return;
			}
			for(var i=0;i<x_len;i++){

				var trace1 = {
		 			x: x_values_list[i], 
		  			y: y_values_list[i], 
		  			type: 'scatter'
				};
				data.push(trace1);
			}

			var layout1 = {
				xaxis: {
    				title: 's',
  				},
	  			yaxis: {
	       			title: serie["symbol"],
	       		},
	     		showlegend: true
			};
			console.log(data);
			Plotly.newPlot(TESTER, data, layout1);
		},
		
	},
})


