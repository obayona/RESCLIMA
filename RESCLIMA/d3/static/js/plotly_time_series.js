// ******************************************************************
// ************************* Simple function ************************
// ******************************************************************

/**
 * Function that transform the size input to return an int
 * @param {Size of the chart on the plugin it could be 7x7, 6x6, ... in str} str 
 */
function getChartPluginSize(str) {
    return parseInt(str[str.length-1]);
  }
  
  /**
   * Funcion that sets the size of the graph
   * @param {Size of the graph container} size 
   */
  function getTimeChartViewBox(size) {
	if (size == 4) { return { sizew : 320, sizeh : 200} }
	else if (size == 5) { return { sizew : 385, sizeh : 280} }
	else if (size == 6) { return { sizew : 470, sizeh : 350} }
	else { return { sizew : 560,  sizeh : 420} }
  }

  /**
   * Returns stations metadata
   * @param {Station object} station 
   */
  function getMetaDataStations(station){
    var url = "/series/stations/";
    var request = $.get(url);
    var self = this;
    request.done(function(data){
      station["stations"] = data["stations"]
    })
  }
  
  /**
   * Function that gets the meteorological stations nedded for the chart
   * @param {str that allows to check if it involves stations} stations
   */
  function getStations(stations, init_date, last_date,size){

    var measure = stations.startsWith("variable_id") ?  
        {"id" : stations.split("=")[1],"exist" : true,
        "ini_date":init_date,"end_date":last_date,'size':getChartPluginSize(size)} :  {"exist":false}
    getMetaDataStations(measure)
    return measure
  }

  /**
   * Function that looks if the date is correctly saved
   * @param {start date to look for data} start_date 
   * @param {final date to look for data} end_date 
   */
  function checkDate(start_date, end_date) {
     if (!isEmpty(start_date) && !isEmpty(end_date)) { return true; }
    else { return false; }
  }
  

  function plotlyWrapperTimeSeries(container, size, source, rangeLabel, start_date, end_date){
    if (!checkDate(start_date, end_date)) {
      // Una de las fechas ingresadas no es valida
      start_date = null;
      end_date = null;
    }
    
    var station = getStations(source,start_date,end_date,size)
    var barcontainer = document.getElementById(container); 
    if(station.exist){
      getVariableInfo(station,barcontainer,size)
    }else{
      plotlyTimeSeries(container, size, source, rangeLabel, start_date, end_date)
    }
  }

  /**
   * Function that draws the TimeSeries
   * @param {id of the container} container 
   * @param {size of the container it could be 5x5, 4x4 ...} size 
   * @param {api endpoin} source 
   * @param {label located on the range line} rangeLabel 
   * @param {start date to look for data} start_date 
   * @param {final date to look for data} end_date 
   */
  function plotlyTimeSeries(container, size, source, rangeLabel, start_date, end_date) {
    
    var datay = [],
        data_dates = [];
  
    // Define URL for JSON
    SOURCE_URL = "/api/" + source + "/" + start_date + "/" + end_date + "/";
    
    var barDiv = document.getElementById(container);
    
    Plotly.d3.json(SOURCE_URL, function(error, data) {
        data.forEach(function(item){
            datay.push(item.count);
            data_dates.push(d3.time.format("%Y-%m-%d").parse(item.month));
          })

          var trace1 = {
            type: "scatter",
            mode: "lines",
            name: rangeLabel,
            x: data_dates,
            y: datay,
            line: {color: '#17BECF'}
          }

          var data = [trace1];
          
          var two_sizes = getTimeChartViewBox(getChartPluginSize(size));
          
          var layout = {
            xaxis: {
              autorange: true,
              range: [data_dates[0], data_dates.slice(-1)[0] ],
              rangeselector: {
                  buttons:[
                  {
                    count: 1,
                    label: 'day',
                    step: 'day',
                    stepmode: 'backward',
                  },  
                  {
                    count: 1,
                    label: 'month',
                    step: 'month',
                    stepmode: 'backward'
                  },
                  {
                    count: 1,
                    label: 'year',
                    step: 'year',
                    stepmode: 'backward'
                  },
                  {step: 'all'}
                ]},
              rangeslider: {range: []},
              type: 'date'
            },
            yaxis: {
              title: rangeLabel,
              type: 'linear'
            },
            width: two_sizes.sizew,
            height: two_sizes.sizeh,  
            paper_bgcolor:'rgba(0,0,0,0)',
            plot_bgcolor:'rgba(0,0,0,0)',  
            margin: {
                l: 40,
                r: 0,
                b: 10,
                t: 50,
                pad: 2
              },
          };
          
          Plotly.newPlot(barDiv, data, layout);
      
    });

}

/**Parte para renderizacion de Datos de estaciones meteorologicas */

var measurements = {"limit":100, "offset":0, "max_offset":-1}
//TODO change global variable to other name and use that to fix limits and go next and back

function download(variable){
  var url = "/series/measurements/download/?variable="
  var variable_str = variable.id + "["
  var length = variable.stations.length - 1;
  for(var i=0;i< length;i++){
    var station = variable.stations[i];
    variable_str += station.id + "," 
  }
  var station = variable.stations[length];
  variable_str += station.id + "]"
  url += variable_str;

  if(variable["ini_date"]){
    url = url + "&ini_date=" + variable["ini_date"];
  }
  if(variable["end_date"]){
    url = url + "&end_date=" + variable["end_date"];
  }
  
  return url;
}
/*
Realiza una peticion ajax para 
obetenr los metadados de una variable*/
function getVariableInfo(variable,container,size){
	var url = "/series/variable/info/"+variable.id;
	var request = $.get(url);
	var self = this;
	request.done(function(data){
		variable["name"]=data["name"];
		variable["unit"]=data["unit"];
		variable["symbol"]=data["symbol"];
		variable["datatype"]= data["datatype"];
    variable["state"]="loaded";
    variable["size"] = size;
		// se inicializa el plot
    self.initializePlot(variable,container,size);
    addnextOptions(measurements,container,variable)
		// se piden los datos solo si el tipo de 
		// dato es float
		if(variable["datatype"]=="float"){
			self.getMeasurements(variable,container);	
		}
		
	});
	request.fail(function(data){
		console.log("lo hago failed",variable);
		variable.state = 'failed';
	});
}
/*
Por cada estacion de la variable,
pide los datos de la estacion
*/
function getMeasurements(variable,container){

  var stations = variable["stations"];
  var station = {}
	for(var i=0; i<stations.length; i++){
    station.id = stations[i]
    station.name = stations[i]
		this.getStationMeasurements(variable,station,container,station.id);
	}
}
/*
Pide la serie de tiempo de una estacion.
*/
function getStationMeasurements(variable,station,container,idSta){
  var self = this;
  this.limit = 100,
      offset = 0,
      max_offset =-1;
	// se crea el url			
	var url = "/series/measurements/?";
	url += "variable_id="+variable["id"];
	url += "&station_id="+station["id"];
	if(variable["ini_date"]){
		url +="&ini_date="+variable["ini_date"];
	}
	if(variable["end_date"]){
		url +="&end_date="+variable["end_date"];
  }
	url+="&limit="+this.measurements.limit;
  url+="&offset="+this.measurements.offset
	var request = $.get(url);
  station["state"]="loading";
	request.done(function(response){
   
		var response_measures = response["measurements"];
		// se actualiza
    var full_count = response["full_count"];
    self.max_offset = full_count - self.limit;
    measurements.max_offset = self.max_offset;
/*    measurements.limit = 100;
    measurements.offset = 0;*/
    
		if(full_count>0){
      self.assingMeasurements(station,response_measures);  
      // dibuja el plot
      self.addTrace(variable,station,container, idSta);              	
		}
  });
  
	request.fail(function(response){
    station["state"]="failed";

  });
  
}
/*
Asigna la serie de tiempo a la estacion
*/
function assingMeasurements(station,measurements){

  station["x_values"] = [];
  station["y_values"] = [];
	for(var i=0;i<measurements.length; i++){
		var m = measurements[i];
		station["x_values"].push(m["ts"]);
		station["y_values"].push(m["value"]);
	}
	station["state"]="loaded";
}
/*
Inicializa el plot usando la libreria Plotly
*/
function initializePlot(variable, container,size){
	var data = []
  var y_title = variable["unit"]+ " ( " + variable["symbol"] + " )";
  var two_sizes = getTimeChartViewBox(getChartPluginSize(size));
	var layout = {
		showlegend: true,
    autosize:true,
    width: two_sizes.sizew,
    height: two_sizes.sizeh,  
    paper_bgcolor:'rgba(0,0,0,0)',
    plot_bgcolor:'rgba(0,0,0,0)',  
		margin: {
			l: 50,
			r: 10,
			b: 50,
			t: 50,
			pad: 4
		},
		yaxis:{title: y_title}
	};
	Plotly.newPlot(container,data,layout,{responsive: true});
	// se actualiza el plot
	Plotly.Plots.resize(container);
}
/*
Agrega una traza al plot
*/
function addTrace(variable,station,container,idSta){
  var container = container;
	var data = container.data;
	var n_traces = data.length;
	//change dates according to time zone
	for (var i = 0; i < station["x_values"].length; i++) { 
		station["x_values"][i] = new Date(Date.parse(station["x_values"][i]+"+0000"));
  }

	station["trace_index"]=n_traces;
	// se crea el trace
	var trace = {
		x:station["x_values"],
		y:station["y_values"],
		type: 'scatter',
		name: 'Estacion '+idSta,
		line:{color:station["color"]},
		visible:station["visible"]
	};
	Plotly.addTraces(container,[trace]);
}
/*
Handler del boton prev, en la
paginacion. Trae los anteriores datos
*/
function prev(measures, container,variable){
  if(measurements.offset <= 0){
    console.log($(container).find("#prev"))
    return;
  }
  this.measurements.offset -= this.measurements.limit;
  initializePlot(variable,container,variable.size);
  getMeasurements(variable,container);
}
/*
Handler del boton next, en la
paginacion. Trae los siguiente datos
*/
function next(measures,container,variable){

  if(measurements.offset>=measurements.max_offset){
    console.log($(container).find("#next"))
    return;
  }
  this.measurements.offset += this.measurements.limit;
  initializePlot(variable,container,variable.size);
  getMeasurements(variable,container);
}

/**
 * Function to update the traces for moving to future or past positions
 * @param {*} metadata 
 * @param {*} container 
 * @param {*} variable 
 */
function addnextOptions(metadata,container,variable){

  var containerID = "#"+container.id+'-nextpast'
  $(containerID).empty() 
  var preLbl = $('<div/>', {
    'id':'myDiv',
    'class':'col s4',
    'style':'center;cursor:pointer;font-weight:bold;',
    'html':'<a href="#!"><i class="material-icons">chevron_left</i></a>',
    'mouseenter':function(){ $(this).css('color', 'blue'); },
    'mouseleave':function(){ $(this).css('color', 'black'); }
  }).appendTo(containerID);
  
  var nextLbl = $('<div/>', {
    'id':'next',
    'class':'col s4',
    'style':'center;cursor:pointer;font-weight:bold;',
    'html':'<a href="#!"><i class="material-icons">chevron_right</i></a>',
    'mouseenter':function(){ $(this).css('color', 'blue'); },
    'mouseleave':function(){ $(this).css('color', 'black'); }
  }).appendTo(containerID);

  $(nextLbl).click(function(){
    next(metadata,container,variable)
  })

  $(preLbl).click(function(){
    prev(metadata,container,variable)
  })

}