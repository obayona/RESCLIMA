// ******************************************************************
// ************************* Simple function ************************
// ******************************************************************

function toTitleCase(str) {
    return str.replace(/\w\S*/g, function(txt){
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}

function getChartPluginSize(str) {
  return parseInt(str[str.length-1]);
}

function getPieChartViewBox(size) {
	if (size == 4) { return {sizew:300, sizeh:200} }
	else if (size == 5) { return {sizew:400,sizeh:265} }
	else if (size == 6) { return {sizew:400,sizeh:320} }
	else { return {sizew:400,sizeh:400} }
}

function isEmpty(str) {
	if (!str) { return true; }
	else { return false }
}

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

  var two_sizes =  getPieChartViewBox(getChartPluginSize(size))

  var layout = {
      autosize: true,
      paper_bgcolor: "rgba(0,0,0,0)",
      width: two_sizes.sizew,
      height: two_sizes.sizeh,
      margin: {
        l: 10,
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

function changePieButton(valuesP,labelsP, container,baseDiv,size, source){

  var bars = document.getElementById("ibarp-"+baseDiv.id.slice(6,baseDiv.id.length));
  var pieDiv = document.getElementById("ipie-"+baseDiv.id.slice(6,baseDiv.id.length));

	bars.addEventListener('click',function(){
		$("#"+container).empty();
		transform_to_bars_from_p(valuesP, labelsP,baseDiv,size)
  });

	pieDiv.addEventListener('click', function(){
		$("#"+container).empty();
		transform_back_to_pie_chart(valuesP,labelsP,baseDiv,size,source)
	});	
}


function transform_to_bars_from_p(valuesP, labelsP, barDiv,size){

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
