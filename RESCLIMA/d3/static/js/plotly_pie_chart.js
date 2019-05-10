// ******************************************************************
// ************************* Simple function ************************
// ******************************************************************

function getChartPluginSize(str) {
  return parseInt(str[str.length-1]);
}

function getChartViewBox(size) {
	if (size == 4) { return {sizew:300, sizeh:200} }
	else if (size == 5) { return {sizew:400,sizeh:265} }
	else if (size == 6) { return {sizew:400,sizeh:320} }
	else { return {sizew:400,sizeh:400} }
}

/**
 * Function that gets the id accordign a tag
 * @param {container's id} container 
 * @param {tag use to tracnsform the id} htmltag 
 */
function getDivId(container, htmltag){
	var idtxt =  container.slice(6,container.length)
	return htmltag+"-"+idtxt;
}

function checkDate(start_date, end_date) {
   if (!isEmpty(start_date) && !isEmpty(end_date)) { return true; }
  else { return false; }
}

function setSourcePieChart(sid, source, start_date, end_date) {
	if (!sid) { return "/api/" + source + "/" + start_date + "/" + end_date; }
	else { return "/api/" + source + "/" + sid; }
}

/**
 * Function that changes the chart to a pie chart
 * @param {data to render the chart} valuesP 
 * @param {labels for the data} labelsP 
 * @param {htmml element} pieDiv 
 * @param {chart's size} size 
 * @param {api endpoint} source 
 */
function transform_back_to_pie_chart(valuesP, labelsP,pieDiv, size,source){
  
  var colorScheme = ["#FF8A65", "#4DB6AC","#FFF176","#BA68C8","#00E676","#AED581","#9575CD","#7986CB","#E57373","#A1887F","#90A4AE","#64B5F6"];
  var traceA = {
    type: "pie",
    values: valuesP,
    labels: labelsP,
    hole: 0.25,
    pull: [0.1, 0, 0, 0, 0],
    direction: 'clockwise',
    marker: {
      colors: colorScheme,
      line: {
        color: 'gray',
        width: 0.1
      }
    },
    textfont: {
      family: 'Lato',
      color: 'white',
      size: 18
    },
    hoverlabel: {
      bgcolor: 'black',
      bordercolor: 'gray',
      font: {
        family: 'Lato',
        color: 'white',
        size: 18
      }
    }
  };
  var data = [traceA];

  var two_sizes =  getChartViewBox(getChartPluginSize(size))

  var layout = {
      autosize: true,
      width: two_sizes.sizew,
      height: two_sizes.sizeh,
      paper_bgcolor:'rgba(0,0,0,0)',
      plot_bgcolor:'rgba(0,0,0,0)',
      margin: {
        l: 0,
        r: 0,
        b: 0,
        t: 20,
        pad: 2
      },
  };

  Plotly.plot(pieDiv, data, layout);
  pieDiv.on('plotly_click', function(data){
    var pts = '';
    var selected_path = data.event.target.__data__.label
    applyInteractivity(source,selected_path)
  });
}

/**
 * Function thar draws the pie Chart
 * @param {container's id} container 
 * @param {api endpoint} source 
 * @param {initial date to look for data} start_date 
 * @param {final date to look for data} end_date 
 * @param {graph size} size 
 * @param {SUMO simulation id} sid 
 * @param {description of the graph} description 
 */
function plotlyPieChartSample(container, source, start_date, end_date, size, sid,description){
    if (!checkDate(start_date, end_date)) {
        // Una de las fechas ingresadas no es valida
        start_date = null;
        end_date = null;
      }
      var pieDiv = document.getElementById(container);

      SOURCE_URL = setSourcePieChart(sid, source, start_date, end_date);
      var valuesP = []
      var labelsP = []

      Plotly.d3.json(SOURCE_URL, function(error, data) {
        data.forEach(function(item){
              item.enabled = true; 
              valuesP.push(item.value)
              labelsP.push(item.key)
          });
        transform_back_to_pie_chart(valuesP, labelsP,pieDiv, size,source)
        

      })
}

/**
 * 
 * @param {values for the graph} valuesP 
 * @param {labels of the values for the graph} labelsP 
 * @param {container id} container
 * @param {html element} baseDiv 
 * @param {graph's size} size
 * @param {api endpoint} source 
 */
function changeButton(valuesP,labelsP, container,baseDiv,size, source){

  var bars = document.getElementById("ibarp-"+baseDiv.id.slice(6,baseDiv.id.length));
  var pieDiv = document.getElementById("ipie-"+baseDiv.id.slice(6,baseDiv.id.length));

	bars.addEventListener('click',function(){
		$("#"+container).empty();
		transform_to_bars(valuesP, labelsP,baseDiv,size)
  });

	pieDiv.addEventListener('click', function(){
		$("#"+container).empty();
		transform_back_to_pie_chart(valuesP,labelsP,baseDiv,size,source)
	});	
}

/**
 * 
 * @param {values for the graph} valuesP 
 * @param {labels of the values for the graph} labelsP 
 * @param {html element} barDiv 
 * @param {graph's size} size 
 */
function transform_to_bars(valuesP, labelsP, barDiv,size){

	//var values = values.map(v => v.slice(7, v.length))

	var trace1 = {
		x: labelsP,
		y: valuesP[0],
		name: labelsP[0],
		type: 'bar',
		text: valuesP,
		marker: {
			color: 'rgb(142,152,195)'
		}
	};
  
  var trace2 = {
		x: labelsP,
		y: valuesP[1],
		name: labelsP[1],
		type: 'bar',
		text: valuesP,
		marker: {
			color: 'rgb(142,124,195)'
		}
	};
  
	var data = [trace1, trace2];
	var two_sizes = getChartViewBox(getChartPluginSize(size));
	
	var layout = {
		height: two_sizes.sizeh,
		width: two_sizes.sizew,
		margin: {
			l: 35,
			r: 10,
			b: 30,
			t: 20,
			pad: 2
		},
		font:{
			family: 'Raleway, sans-serif'
		},
		showlegend: true,
		xaxis: {
			tickangle: 0,
			title: ''
		},
		yaxis: {
			zeroline: false,
			gridwidth: 2,
			title: ""
		},
    bargap :0.05,
    barmode: 'stack'
	};

	Plotly.newPlot(barDiv,data,layout);
}

/**
 * Function to redirect accordin to a a click event
 * @param {source of the data} source 
 * @param {path selected} selected_path 
 */
function applyInteractivity(source, selected_path){
  //TODO function that activates on click event and redirection to
  // another chart below the current ones according to the data that is presented
  var fuente = source.split("chart_")[1]
  if(fuente=="censo"){
    window.location.replace("/plot/poblacion/dashboard/");
  }else if(fuente.startsWith("composition")){
    window.location.replace("/plot/logistica/dashboard/")
  }   
}

/**
 * More efficient method to update the graphs
 * @param {container id} container 
 * @param {api endpoint} source 
 * @param {start date to look for data} start_date 
 * @param {end date to look for data} end_date 
 * @param {SUMO simulation id} sid 
 * @param {size of the chart} size 
 */
function updatePieDate(container, source, start_date, end_date, sid, size){
  SOURCE_URL = setSourcePieChart(sid, source, start_date, end_date);
  var pieDiv = document.getElementById(container);
  var colorScheme = ["#FF8A65", "#4DB6AC","#FFF176","#BA68C8","#00E676","#AED581","#9575CD","#7986CB","#E57373","#A1887F","#90A4AE","#64B5F6"];
  var valuesP = [],
      labelsP = [];
  Plotly.d3.json(SOURCE_URL, function(error, data) {
    data.forEach(function(item){
          item.enabled = true; 
          valuesP.push(item.value)
          labelsP.push(item.key)
      });
      var traceA = {
        type: "pie",
        values: valuesP,
        labels: labelsP,
        hole: 0.25,
        pull: [0.1, 0, 0, 0, 0],
        direction: 'clockwise',
        marker: {
          colors: colorScheme,
          line: {
            color: 'gray',
            width: 0.1
          }
        },
        textfont: {
          family: 'Lato',
          color: 'white',
          size: 18
        },
        hoverlabel: {
          bgcolor: 'black',
          bordercolor: 'gray',
          font: {
            family: 'Lato',
            color: 'white',
            size: 18
          }
        }
      };
      var data_update = [traceA];
    
      var two_sizes =  getChartViewBox(getChartPluginSize(size))
    
      var layout_update = {
          autosize: true,
          width: two_sizes.sizew,
          height: two_sizes.sizeh,
          margin: {
            l: 0,
            r: 0,
            b: 0,
            t: 20,
            pad: 2
          },
      };

      Plotly.update(pieDiv, data_update, layout_update)
  })
}

/**
 * Function that updates the data according to a date
 * @param {id of the input that has the first date} id_first_date 
 * @param {id of the input that has the last date to look for data} id_last_date 
 * @param {container's id} container 
 * @param {api endpoint} source 
 * @param {container's size} size 
 * @param {SUMO simulation id} sid 
 * @param {description of the graph} description 
 */
function changePieDate(id_first_date,id_last_date, container, source, size, sid,description){
  value = $("#"+id_first_date).val();
  value_new = $("#"+id_last_date).val()
  start_date = value == ""? null: new Date(value).toISOString().slice(0,10) 
  end_date = value_new == "" ? null : new Date(value_new).toISOString().slice(0,10)   
  if(start_date!==null && end_date!==null){
    updatePieDate(container, source, start_date, end_date, sid, size);
  }
}