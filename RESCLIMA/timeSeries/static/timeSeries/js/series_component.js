
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

		var colors = ['#1f77b4','#ff7f0e','#2ca02c',
					  '#d62728','#9467bd','#8c564b',
					  '#e377c2','#7f7f7f','#bcbd22',
					  '#17becf']

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
				var color = colors.shift();
				station["color"]=color;
				colors.push(color);
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
		
	}
})


