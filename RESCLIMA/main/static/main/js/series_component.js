Vue.component("series_component",{
	// este componente debe reaccionar al arreglo de resultados
	// this.shared.series

	//PONER COMO DESCRIPCION NUMERO DE ESTACIONES
	
	template: `
		<div>
			<!-- Si el estado de las series es searched-->
			<!-- Se muestran las series-->
			<div v-if="shared.series_state=='searched'">
				<div v-if="shared.series.length > 0">
					<div>
						<a
						class="btn waves-effect waves-light gradient-45deg-light-blue-cyan" 
						v-bind:disabled="selected_count==0" v-on:click="visualizarSeries">
							<i class="material-icons left">remove_red_eye</i>Visualizar</a>
						<a
						class="btn waves-effect waves-light gradient-45deg-light-blue-cyan" 
						v-bind:disabled="selected_count==0">
							<i class="material-icons left">file_download</i>Descargar</a>
					</div>
					<div v-for="serie in shared.series">
						<div class="card">
							<div class="card-content">
								<span class="card-title">
									<input
									type="checkbox"
									v-bind:id="serie.variable_id"
									v-bind:value="serie.selected"
									v-on:input="selectSerie(serie)">
									<label v-bind:for="serie.variable_id"></label>
									{{serie.variable_name}}
								</span>
								<p>Se han encontrado {{serie.amount_stations}} estaciones en la búsqueda.</p>
							</div>
						</div>		
					</div>
				</div>
				<div v-else>No hay resultados</div>
			</div>
			<!-- si el estado de las series es loading se -->
			<!-- muestra una animacion -->
			<div v-if="shared.series_state=='loading'">
				<div v-if="shared.state=='loading'">
					<div class="preloader-wrapper big active">
						<div class="spinner-layer spinner-blue-only">
							<div class="circle-clipper left">
								<div class="circle"></div>
							</div>
							<div class="gap-patch">
								<div class="circle"></div>
							</div>
							<div class="circle-clipper right">
								<div class="circle"></div>
							</div>
						</div>
					</div>
				</div>
			</div>
			<!-- si el estado de las series es fail se -->
			<!-- muestra un mensaje de error -->
			<div v-if="shared.series_state=='fail'">
				<div class="red">
					<b>Ha ocurrido un error</b>
				</div>
			</div>

		</div>			
	`,
	data(){
		return {
			selected_count:0,
			shared:store
		}
	},
	methods:{
		selectSerie(serie){
			console.log("check serie",serie)
			serie.selected = !serie.selected;
			if(serie.selected==true) 
				this.selected_count +=1;
			if(serie.selected==false)
				this.selected_count -=1;
		},
		visualizarSeries(){
			//redirect to the url to visualize the selected time series
			var url = "series/view/" + this.shared.getSeriesParams();
			console.log("Url de series a visualizar: "+ url)
			//this.$router.replace(url);
			//this.$router.go();
			url = encodeURI(url)
			window.open(url,'_blank');
		},
		
	}
})

