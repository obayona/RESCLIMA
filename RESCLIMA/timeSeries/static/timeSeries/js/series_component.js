
Vue.component("series_component",{
	template: `
		<div>
			<div v-if="shared.series.length>0">
			

				<!-- Contenedor de la serie -->
				<!-- se itera sobre el array shared.series -->
				<div v-for="serie in shared.series"
				class="card" >
					<!-- Si la capa tiene estado uninitialized-->
					<!-- Se muestran animaciones-->
					<div v-if="serie.state=='uninitialized'">
						<div style="width:100px;height:20px;margin:10px;" class="animated-background"></div>
						<div style="width:200px;height:20px;margin:10px;" class="animated-background"></div>
						<div style="width:20px;height:20px;margin:10px;" class="animated-background"></div>
					</div>
					
					<!-- Si la serie tiene estado distinto a uninitialized-->
					<!-- Se muestran los metadatos de la serie -->
					<div v-else>
						<h5>{{serie.variable_name}} vs tiempo</h5>
						<div v-bind:data-plot-id="serie.variable_id" >
						
							
						</div>
								<!-- Contenedor con opciones de la capa -->
								<!-- Solo se muestra si el estado de la capa es loaded-->
								<!-- Si la serie no tiene estado loaded-->
								<!-- no se muestran las opciones de la serie,-->
								<!-- se muestra una animacion-->
					</div>
					

				</div>
			</div>
			<!-- Si no hay capas en shared.series se muestra un mensaje-->
			<div v-else>
				<p>No hay información de las series</p>
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
   		if(ini_date==null){
   			ini_date = "none";
   		}
   		if(end_date ==null){
   			end_date = "none";
   		}		
		if (!query_string){
			return;
		}

		//parse data
		var variables_info = query_string.split("|");
		var params = {}
		var imax = variables_info.length
		for(var i=0 ; i<imax ; i++){
			//get the variable id
			var current = variables_info[i];
			var variable_id = current.charAt(0);
			if(!variable_id){
				return;
			}
			//get variables of stations
			var estaciones_str = current.slice(2,current.length-1);
			var estaciones = estaciones_str.split(",");
			params[variable_id] = estaciones;
			var serie = {};
			serie["variable_id"]=variable_id;
			serie["variable_name"] = "";
			serie["symbol"] = "";
			serie["x_values"] = [];
			serie["y_values"] =[];
			serie["stations_ids"] = estaciones;
			serie["state"]="uninitialized";
			serie["ini_date"] = ini_date;
			serie["end_date"] = end_date;

			// se guarda el objeto en el store
			// compartido
			this.shared.series.push(serie);
			//graficar
			var divid = serie["variable_id"];
			this.getStationSerie(serie);
			
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
		getStationSerie(serie){
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
			Plotly.newPlot(TESTER, data, layout1);
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
		},*/

  	t(serie){
		var divid = "div"+serie.variable_id;      
        return divid;
      }
		
		
	}
})

