
Vue.component("series_component",{
	template: `
		<div v-if="shared.series.length>0">
			<!-- Contenedor de la serie -->
			<!-- se itera sobre el array shared.series -->
			<div v-for="serie in shared.series"
			class="card">
				<!-- Si la capa tiene estado uninitialized-->
				<!-- Se muestran animaciones-->
				<div v-if="serie.state=='uninitialized'">
					<div style="width:100px;height:20px;margin:10px;" class="animated-background"></div>
					<div style="width:200px;height:20px;margin:10px;" class="animated-background"></div>
					<div style="width:20px;height:20px;margin:10px;" class="animated-background"></div>
				</div>
				<!-- Si la serie tiene estado distinto a uninitialized-->
				<!-- Se muestran los metadatos de la serie -->
				<div v-if="serie.state!='uninitialized'">
					<h5>{{serie.variable_name}} vs tiempo</h5>
							<!-- Contenedor con opciones de la capa -->
							<!-- Solo se muestra si el estado de la capa es loaded-->
							
							<!-- Si la serie no tiene estado loaded-->
							<!-- no se muestran las opciones de la serie,-->
							<!-- se muestra una animacion-->
							<div v-else>
								<div class="animated-background" style="height:80px">Cargando...</div>
							</div>
						</div>
					</div>
				</div>
				<!-- Si no hay capas en shared.series se muestra un mensaje-->
				<div v-else>
					<p>No hay información de las series</p>
				</div>
	`,
	mounted(){
		/* Se lee el parametro "variables" del queryString
		del url, el cual tiene el siguiente formato:
		variables=id_var1[stacion1,stacion2]|id_var2[stacion1]|...|id_varN */
		var query_string = this.$route.query["variables"];
		console.log("QUERY STRING : "+query_string)
		var ini_date = this.$route.query["ini_date"]; 
   		var end_date = this.$route.query["end_date"];
   		//make sure we assign date params a value
   		if(ini_date==null){
   			ini_date = "";
   		}
   		if(end_date ==null){
   			end_date = "";
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
			var divid = "div"+serie["variable_id"];
			this.getStationSerie(serie);
			//this.plotSingleTrace(serie["x_values"], serie["y_values"], divid, serie["variable_name"], serie["symbol"]);
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
		
				});
			}
			
		},	
		
		
	}
})

