
Vue.component("serie_component",{
	template: `
		<div class="card">
			<!-- si el estado es uninitialized -->
			<!-- se muestra una animacion -->
			<div 
			 v-bind:style="[variable.state=='uninitialized'?{'display':''}:{'display':'none'}]">
				<div style="width:100px;height:20px;margin:10px;" class="animated-background"></div>
				<div style="width:200px;height:20px;margin:10px;" class="animated-background"></div>
				<div style="width:20px;height:20px;margin:10px;" class="animated-background"></div>
			</div>
					
			<!-- Si la serie tiene estado distinto a uninitialized-->
			<!-- Se muestran los metadatos de la serie -->
			<div v-bind:style="[variable.state!='uninitialized'?{'display':''}:{'display':'none'}]">
				<div class="card-header cyan accent-4">
					<div class="card-title white-text">
						 <h4 class="card-title">{{variable.name}} vs tiempo</h4>
					</div>
				</div>
				<div class="card-content">
					<!-- Contenedor para el plot-->
					<div class="row">
						<div class="col s10">
							<div v-bind:data-plot-id="variable.id"></div>
						</div>
						<div class="col s2">
							<ul>
								<li v-for="station in variable.stations">
									<strong class="legendSymbol"
										v-bind:style="{'background':station.color}">
									</strong>
									<span>{{"Estación " + station.id}}</span>
								</li>
							</ul>
						</div>
					</div>
					<!-- botones de paginacion -->
					<div class="row"
						v-if="offset != 0 || offset < max_offset">
						<ul class="pagination">
							<li v-bind:class="{disabled: offset == 0}"
							    v-on:click.prevent="prev()">
								<a href="#!">
									<i class="material-icons">chevron_left</i>
								</a>
							</li>
							<li v-bind:class="{disabled: offset >= max_offset}"
							    v-on:click.prevent="next()">
								<a href="#!">
									<i class="material-icons">chevron_right</i>
								</a>
							</li>
						</ul>
					</div>
				</div>

			</div>
			
		</div>
	`,
	props:["variable"],
	mounted(){
		var variable = this.variable;
		var id_variable = variable.id;
		var nodes = document.querySelectorAll('[data-plot-id="'+id_variable+'"]');
		if(nodes.length==0){
			console.log("Error fatal");
			return;
		}
		this.container = nodes[0];
		this.getVariableInfo(variable);
	},

	data(){
		return {
			container:null,
			limit:100,
			offset:0,
			max_offset:-1,
			shared:store,
		}
	},

	methods:{
		getVariableInfo(variable){
			var url = "/series/variable/info/"+variable.id;
			var request = $.get(url);
			var self = this;
			request.done(function(data){
				variable["name"]=data["name"];
				variable["unit"]=data["unit"];
				variable["symbol"]=data["symbol"];
				variable["datatype"]= data["datatype"];
				variable["state"]="metadata_loaded";
				// se inicializa el plot
				self.initializePlot(variable);
				// se piden los datos
				self.getMeasurements(variable);
			});
			request.fail(function(data){
				console.log("Error",data)
			});
		},
		getMeasurements(variable){
			var stations = variable["stations"];
			for(var i=0; i<stations.length; i++){
				var station = stations[i];
				this.getStationMeasurements(variable,station);
			}
		},
		getStationMeasurements(variable,station){
			var self = this;
			var url = "/series/measurements/?";
			url += "variable_id="+variable["id"];
			url += "&station_id="+station["id"];
			if(variable["ini_date"]){
				url +="&ini_date="+variable["ini_date"];
			}
			if(variable["end_date"]){
				url +="&end_date="+variable["end_date"];
			}
			url+="&limit="+this.limit;
			url+="&offset="+this.offset;
			console.log(url);
			var request = $.get(url);
			request.done(function(response){
				var measurements = response["measurements"];
				// se actualiza
				var full_count = response["full_count"];
				self.max_offset = full_count - self.limit;
				
				self.assingMeasurements(station,measurements);
				// dibuja el plot
				self.addTrace(variable,station);
			});
			request.fail(function(response){
				console.log("Error",response);
			});
		},
		assingMeasurements(station,measurements){
			station["x_values"] = [];
			station["y_values"] = [];
			for(var i=0;i<measurements.length; i++){
				var m = measurements[i];
				station["x_values"].push(m["ts"]);
				station["y_values"].push(m["value"]);
			}
		},
		initializePlot(variable){
			// se inicializa el plot

			var data = []
			var y_title = variable["unit"]+ " ( " + variable["symbol"] + " )";
			var layout = {
				showlegend: false,
				autosize:true,
				margin: {
					l: 50,
					r: 10,
					b: 50,
					t: 50,
					pad: 4
				},
				yaxis:{title: y_title}
			};
			Plotly.newPlot(this.container,data,layout,{responsive: true});
			Plotly.Plots.resize(this.container);
		},
		addTrace(variable,station){
			var container = this.container;

			// se crea el trace
			var trace = {
				x:station["x_values"],
				y:station["y_values"],
				type: 'scatter',
				name: 'Estacion '+station["id"],
				line:{color:station["color"]}
			};
			Plotly.addTraces(container,[trace]);
		},
		prev(){
			if(this.offset <= 0){
				return;
			}
			this.offset -= this.limit;
			var container = this.container;
			var variable = this.variable;
			this.initializePlot(variable);
			this.getMeasurements(variable);
		},
		next(){
			if(this.offset>=this.max_offset){
				return;
			}
			this.offset += this.limit;
			var container = this.container;
			var variable = this.variable;
			this.initializePlot(variable);
			this.getMeasurements(variable);
		}
	},
})



