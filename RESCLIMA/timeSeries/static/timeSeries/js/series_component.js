
Vue.component("series_component",{
	template: `
		<div>
			<div v-if="shared.variables.length>0">
			
				<!-- Contenedor de la serie -->
				<!-- se itera sobre el array shared.series -->
				<div v-for="variable in shared.variables">
					<serie_component v-bind:variable="variable"></serie_component>
				</div>
			</div>
			<div v-else>
			No hay series de tiempo
			</div>
		
		</div>
	`,
	mounted(){
		/* Se lee el parametro "variables" del queryString
		del url, el cual tiene el siguiente formato:
		variables=id_var1[stacion1,stacion2]|id_var2[stacion1]|...|id_varN */
		var query_string = this.$route.query["variables"];
		var ini_date = this.$route.query["ini_date"]; 
		var end_date = this.$route.query["end_date"];
		//make sure we assign date params a value
		if(!ini_date){
			ini_date = null;
		}
		if(!end_date){
			end_date = null;
		}		
		if (!query_string){
			return;
		}

		//parse data
		var variables_str = query_string.split("|");
		for(var i=0 ; i < variables_str.length; i++){
			//get the variable id
			var variable_str = variables_str[i];
			var j = variable_str.indexOf("[");
			var k = variable_str.indexOf("]");
			if(j<0 || k<0){
				continue;
			}

			var variable_id = variable_str.slice(0,j);
			var stations_str = variable_str.slice(j+1,k);

			var stations_id = stations_str.split(",");
			
			var variable = {};

			variable["id"]=variable_id;
			variable["name"] = "";
			variable["unit"]="";
			variable["symbol"] = "";
			variable["datatype"]="";
			variable["ini_date"] = ini_date;
			variable["end_date"] = end_date;
			// se crean las estaciones
			variable["stations"] = []
			for(var j=0; j<stations_id.length;j++){
				var station = {}
				station["id"]=stations_id[j]
				station["x_values"]=[];
				station["y_values"]=[];
				variable["stations"].push(station);
			}
			variable["state"]="uninitialized";

			// se guarda el objeto en el store
			// compartido
			this.shared.variables.push(variable);
		}

	},
	data(){
		return {
			shared:store		
		}
	},
	methods:{
		/*Metodo que realiza una peticion ajax
		para obtener los datos de una sola estacion de una variable*/
		/*getStationSerie(serie){
			var id_variable = serie["variable_id"];
			var ini_date = serie["ini_date"];
			var end_date = serie["end_date"]
			// referencia al componente
			var self = this;
			for(var i=0;i<serie["stations_ids"].length;i++){
				var current = serie["stations_ids"][i];
				var url = "/series/measurements/"+id_variable+"/"+current+"/"+ini_date+"/"+end_date+"/";
				// peticion GET
				var request = $.get(url);
				request.done(function(data){
					serie["x_values"].push(data["series"]["dates"]);
					serie["y_values"].push(data["series"]["measurements"]);
					serie["variable_name"] = data["series"]["variable_name"];
					serie["symbol"] = data["series"]["variable_symbol"];
					// se actualiza el estado de la serie
					serie["state"]="metadata_loaded";
					self.plotSingleTrace(serie);
		
				});
				
			}
			
		},	
		plotSingleTrace(serie){
			if(serie["state"]=="uninitialized"){
				console.log("uninitialized");
				
			}
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
			Plotly.react(TESTER, data, layout1);
		},
		/*plotSingleTrace(x_values, y_values,div_id, y_title, symbol){
			if(serie)
			var TESTER = document.querySelectorAll("[data-plot-id=\'"+div_id+"\']")[0];
			//var TESTER = document.querySelectorAll("[data-plot-id='5']")[0];
			console.log("[data-plot-id=\'"+div_id+"\']");
			console.log(TESTER);
			//var TESTER =  $('[data-plot-id=\"'+div_id+'\"]');
			var data = [];
			var trace = {
		 			x: x_values, 
		  			y: y_values, 
		  			type: 'path'
				};
			var layout1 = {
				title:y_title+" vs tiempo",
				xaxis: {
	    			title: 's',
	    			
	  			},
		  		yaxis: {
		       		title: symbol,
		     	},
		     	showlegend: true
			};
			data.push(trace);
			Plotly.newPlot(TESTER, data, layout1);
		},

  	t(serie){
		var divid = "div"+serie.variable_id;      
        return divid;
      }*/
		
		
	}
})


