var clima_component = Vue.component("clima_component",{

  template:
  `
  <div class='row'>
    <h4 class="text-grey text-lighten-4 col s12">Informaci&oacute;n Climatol&oacute;gica</h4>
    
    <div class="z-depth-3">
      <h5 class="text-grey text-lighten-4 col s12">Valores de Estaciones Meteorol&oacute;gicas</h5>
      <!--<select id="sta" class = "col s5" @change="handleChange()">
        <option v-for="station in stations" v-bind:value= "{ var : station.name }">
        {{station.complete_name}}</option>
      </select>-->

      <input class = "col s3 ml-2" id="init_date" type="date" 
      v-model="ini_date" @change="updateIniDate" 
      data-date-format='yyyy-mm-dd' >
      </input>
      
      <input class = "col s3 ml-2" id="last_date" type="date" 
      v-model="end_date" @change="updateEndDate" 
      data-date-format='yyyy-mm-dd'  >
      </input>

      <div class="col s12">
        <button type="button" class="mr-1 mb-2 btn btn-primary btn-sm blue accent-1" :id="station.name" v-for="station in stations"
        v-on:click="handleChange(station.name)">{{station.complete_name}}
        <i class="material-icons left">cloud</i></button>
      </div>

      <div class="row">
        <div class="col s8">
          <div id="estacion_graph"></div>
          <div class='col s8' id='estacion_graph-nextpast'></div>
        </div>
        <div class="col s4 z-depth-1">
          <h4>Descripci&oacute;n</h4>
          <h5>
              Datos de estaciones clim&aacute;ticas.
              Se colocaron estaciones climatol&oacutegicas, de tipos
              HOBO y BloomSky, cuyos valores por el tiempo, puedes visualizar
          </h5>
        </div>
      </div>
    </div>

      <div class="z-depth-3">
        <h5 class="text-grey text-lighten-4 col s12">Precipitaciones Anuales</h5>  
        <div>
          <div class="ml-2 col s7">
            <span class="text-center" id="chart-cli1Graf"></span>
          </div>
          <div class="col s4 z-depth-1">
            <h4>Descripci&oacute;n</h4>
            <h5>
                Datos de estaciones clim&aacute;ticas
            </h5>
          </div>
        </div>
      </div>

      <div class="z-depth-3">
      <h5 class="text-grey text-lighten-4 col s12">Factores de Riesgo</h5>
        <div class="row">
          <div class="ml-2 col s7">
          <span class="center " id="chart-cli2Graf"></span>
          <div class = "row text-center " id='div-cli2Graf'>
            <i class='mt-2 material-icons center waves-effect waves-light left' data-toggle="tooltip" data-placement="right" data-html="true" title="Descripcion: <p>
            Factores de Riesgo</p>" >info</i>
            <input id="groupTime-cli2Graf" placeholder="init date" type= "date" class="ml-3 col s5 center"  
            v-model="date_init" @change="riskUpdateDate" 
            :config="config" data-date-format='yyyy-mm-dd'  >
            <input id="grouplastTime-cli2Graf" placeholder="last date" type= "date" class=" col s5 center"  
            v-model="date_final" @change="riskUpdateDate" 
            :config="config"
            data-date-format='yyyy-mm-dd'  > 
            <i id="igroup-cli2Graf" class=" waves-effect waves-light material-icons center" data-toggle="tooltip" data-placement="top" title="GroupBar" >domain</i>
            <i id="iline-cli2Graf" class=" waves-effect waves-light material-icons center" data-toggle="tooltip" data-placement="top" title="LineChart" >dehaze</i>
          </div>
          </div>
          <div class="col s4 z-depth-1">
            <h4>Descripci&oacute;n</h4>
            <h5>
              Datos referentes al factor de Riesgo
            </h5>
          </div>
        </div>
      </div>
      
      <div class="z-depth-3">
          <h5 class="text-grey text-lighten-4 col s12">ONI</h5>
        <div class="row">
          <div class="ml-2 col s7 ">
            <span class="text-center" id="chart-cli3Graf"></span>
          </div>
          <div class="col s4 z-depth-1">
            <h4>Descripci&oacute;n</h4>
            <h5>
                Datos de estaciones clim&aacute;ticas
            </h5>
          </div>
        </div>
      </div>
  
  </div>
  `,
  data(){
  return {
    date_init : null,
    date_final: null,
    config: {
      altFormat: "F j, Y",
      altInput: false
    },
    state:'initial',
    ini_date:null,
    end_date:null,
    station_var:"variable_id=1",
    max_offset:-1,
    stations : [
      temp = {name:"variable_id=1",
              complete_name:"Temperatura"}, 
      hum = {name:"variable_id=2",
              complete_name: "Humedad relativa" },
      lum = {name:"variable_id=7",
              complete_name: "Luminancia"},
      pre = {name:"variable_id=10",
              complete_name:"Presion"},
      uv =  {name:"variable_id=11",
              complete_name: "Indice"} 
      ]
  }
  },
mounted(){

  plotlyWrapperTimeSeries("estacion_graph", "d3_time_series_7x7", "variable_id=1", "Stations", null, null)
  plotlyMultiTimeSeries("chart-cli1Graf", "d3_multi_time_series_7x7", "d3_time_series_tmax", "d3_time_series_tmin", "d3_time_series_tmean", "C", null, null);
  plotlyGroupedBarChart("chart-cli2Graf", "d3_grouped_bar_chart", null, null,"Precipitacion", "d3_grouped_bar_chart_7x7");
  plotlyTimeSeries("chart-cli3Graf", "d3_time_series_7x7", "d3_time_series_oni", "ONI", null, null)

  },
  methods:{
    handleChange(variable) {
      this.station_var = variable;
      plotlyWrapperTimeSeries("estacion_graph", "d3_time_series_7x7", variable, "Stations", this.ini_date, this.end_date)
    },

    riskUpdateDate(selectedDates, dateStr, instance){       
      plotlyGroupedBarChart("chart-cli2Graf", "d3_grouped_bar_chart", this.date_init, this.date_final,"Precipitacion", "d3_grouped_bar_chart_7x7");
    },

    changeMeasurementData(variable){
      plotlyWrapperTimeSeries("estacion_graph", "d3_time_series_7x7", variable, "Stations", null, null)
    },
    updateIniDate(ini_date){
      console.log(this.ini_date)
      plotlyWrapperTimeSeries("estacion_graph", "d3_time_series_7x7", this.station_var, "Stations", this.ini_date, this.end_date)
		},
		updateEndDate(end_date){
      plotlyWrapperTimeSeries("estacion_graph", "d3_time_series_7x7", this.station_var, "Stations", this.ini_date, this.end_date)
		}

  }
})

const router = new VueRouter({
  mode: 'history'
})

// app principal
var app = new Vue({
    router,
    delimiters: ['[[', ']]'],
    el:'#mainViews',
    data:{
      station_var:null,
    },
    methods:{

    }

})