var poblacion_component = Vue.component("poblacion_component",{

    template:
    `
    <div class='row'>
        <div class="card">
          <div class="card-content">
            <p>Informacion adquirida sobre poblacion</p>
          </div>
          <div class="card-tabs">
            <ul class="tabs tabs-fixed-width">
              <li class="tab"><a href="#test4pob">Test 1</a></li>
              <li class="tab"><a class="active" href="#test5pob">Test 2</a></li>
              <li class="tab"><a href="#test6log">Test 3</a></li>
            </ul>
          </div>
          <div class="card-content grey lighten-4">
            <div id="test4pob">
                <div class="row">
                    <div class="col 5">
                        <h3>Descripci&oacute;n</h3>
                        <h4>
                            Se presentan los datos respecto a valores
                            de censos tomados en el Ecuador, tomando
                            en consideraci&oacute;n los aspectos de distribuci&oacute;n
                            entre hombres y mujeres, nivel de analfabetismo y de
                            vivienda
                        </h4>
                    </div>
                    <div class="col 7" id="pobInit">
                        <span div="chart-pob1Graf"><span>
                        <input id="pieTime-chart-pob1Graf" placeholder="init date" type= "text" class="ml-3 col s5 datepicker center"  data-date-format='yyyy-mm-dd'  >
                        <input id="pielastTime-chart-pob1Graf" placeholder="last date" type= "text" class=" col s5 datepicker center"  data-date-format='yyyy-mm-dd'  > 
                    </div>
                </div>

            </div>
            <div id="test5pob">
                <div class="row">
                    <div class="col 5">
                    <h3>Descripci&oacute;n</h3>
                    <h4>
                        Se presentan los datos respecto a valores
                        de censos tomados en el Ecuador, tomando
                        en consideraci&oacute;n los aspectos de distribuci&oacute;n
                        entre hombres y mujeres, nivel de analfabetismo y de
                        vivienda
                    </h4>
                    </div>
                    <div class="col 7" id="pobInit">
                    </div>
                </div>
            </div>
            <div id="test6pob">
                <div class="row">
                    <div class="col 5">
                    </div>
                    <div class="col 7" id="pobInit">
                    </div>
                </div>            
            </div>
          </div>
        </div>
    </div>
    `,
    data(){
		return {

		}
    },
	mounted(){
        plotlyPieChartSample("chart-pob1Graf","d3_pie_chart_censo" , null, null, "d3_pie_chart_7x7", false,"");
    },
    methods:{
        composedGraphs(){

        }
    }
})