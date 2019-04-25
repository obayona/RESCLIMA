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

function getGroupChartViewBox(size) {
	if (size == 4) { return { sizew : 340, sizeh : 230} }
	else if (size == 5) { return { sizew : 410, sizeh : 300} }
	else if (size == 6) { return { sizew : 500, sizeh : 340} }
	else { return { sizew : 570,  sizeh : 410} }
}

function isEmpty(str) {
	if (!str) { return true; }
	else { return false }
}

function checkDate(start_date, end_date) {
   if (!isEmpty(start_date) && !isEmpty(end_date)) { return true; }
  else { return false; }
}

function setSource(source, start_date, end_date) {
	return "/api/" + source + "/" + start_date + "/" + end_date; 
	
}

function transform_back_to_group(valuesX,acumulado, minimo, maximo, promedio, barDiv,size,rangeLabel){

  var trace1 = {
    x: valuesX,
    y: acumulado,
    name: 'Acumulado',
    marker: {color: '#64B5F6'},
    type: 'bar'
  };
  
  var trace2 = {
    x: valuesX,
    y: minimo,
    name: 'Minimo',
    marker: {color: '#A1887F'},
    type: 'bar'
  };
  
  var trace3 = {
    x: valuesX,
    y: maximo,
    name: 'Maximo',
    marker: {color: 'rgb(26, 40 , 255)'},
    type: 'bar'
  };

            
  var trace4 = {
    x: valuesX,
    y: promedio,
    name: 'Promedio',
    marker: {color: "#00E676"},
    type: 'bar'
  };

  var data = [trace1, trace2, trace3, trace4];
  var two_sizes = getGroupChartViewBox(getChartPluginSize(size));
  var layout = {
    title: '',
    xaxis: {
        title: 'years',
        tickfont: {
        size: 14,
        color: 'rgb(107, 107, 107)',
      }},
    yaxis: {
      title: rangeLabel,
      titlefont: {
        size: 16,
        color: 'rgb(107, 107, 107)'
      },
      tickfont: {
        size: 14,
        color: 'rgb(107, 107, 107)'
      },
      paper_bgcolor:'rgba(0,0,0,0)',
      plot_bgcolor:'rgba(0,0,0,0)'
    },

    barmode: 'group',
    bargap: 0.15,
    bargroupgap: 0.1,
    
    width: two_sizes.sizew,
    height: two_sizes.sizeh,

    margin: {
      l: 60,
      r: 50,
      b: 70,
      t: 15,
      pad: 2
    },
  };
  
  Plotly.newPlot(barDiv, data, layout);  
  barDiv.on('plotly_click', function(data){
    window.location.replace('/plot/clima/dashboard')
  });
}

function plotlyGroupedBarChart(container, source, start_date, end_date, rangeLabel, size) {
  if (!checkDate(start_date, end_date)) {
    // Una de las fechas ingresadas no es valida
    start_date = null;
    end_date = null;
  }
  
  SOURCE_URL = setSource(source, start_date, end_date);
  var valuesX = []
  var acumulado = []
  var promedio = []
  var minimo = []
  var maximo = []

  groupBarDiv = document.getElementById(container);
  console.log(groupBarDiv)
  var colorScheme = ["#FF8A65", "#4DB6AC","#FFF176","#BA68C8","#00E676","#AED581","#9575CD","#7986CB","#E57373","#A1887F","#90A4AE","#64B5F6"];
  Plotly.d3.json(SOURCE_URL, function(error, data) {
        data.forEach(function(item){
              valuesX.push(item.categorie)
              acumulado.push(item.values[0].value)
              minimo.push(item.values[1].value)
              maximo.push(item.values[2].value)
              promedio.push(item.values[3].value)
        })

        transform_back_to_group(valuesX,acumulado, minimo, maximo, promedio, groupBarDiv,size,rangeLabel);

        changeGroup(valuesX,acumulado, minimo, maximo, promedio, groupBarDiv,size,container,rangeLabel);
    
  })

}

function changeGroup(valuesX,acumulado, minimo, maximo, promedio, barDiv,size,container,rangeLabel){
	var gbarDiv = document.getElementById("igroup-"+barDiv.id.slice(6,barDiv.id.length));
	var lineDiv = document.getElementById("iline-"+barDiv.id.slice(6,barDiv.id.length));
	lineDiv.addEventListener('click',function(){
		$("#"+container).empty();
		changetoStack(valuesX,acumulado, minimo, maximo, promedio, barDiv,size,rangeLabel)
	})
	gbarDiv.addEventListener('click', function(){
		$("#"+container).empty();
		transform_back_to_group(valuesX,acumulado, minimo, maximo, promedio, barDiv,size,rangeLabel)
	})

}


function changetoStack(valuesX,acumulado, minimo, maximo, promedio, barDiv,size,rangeLabel){

  var trace1 = {
    x: valuesX,
    y: acumulado,
    name: 'Acumulado',
    marker: {color: '#64B5F6'},
    type: 'scatter',
  };
  
  var trace2 = {
    x: valuesX,
    y: minimo,
    name: 'Minimo',
    marker: {color: '#A1887F'},
    type: 'scatter',
  };
  
  var trace3 = {
    x: valuesX,
    y: maximo,
    name: 'Maximo',
    marker: {color: 'rgb(26, 40 , 255)'},
    type: 'scatter',
  };

            
  var trace4 = {
    x: valuesX,
    y: promedio,
    name: 'Promedio',
    marker: {color: "#00E676"},
    type: 'scatter',
  };

  var data = [trace1, trace2, trace3, trace4];
  var two_sizes = getGroupChartViewBox(getChartPluginSize(size));
  var layout = {
    title: '',
    xaxis: {
        title: 'years',
        tickfont: {
        size: 14,
        color: 'rgb(107, 107, 107)',
      }},
    yaxis: {
      title: rangeLabel,
      titlefont: {
        size: 16,
        color: 'rgb(107, 107, 107)'
      },
      tickfont: {
        size: 14,
        color: 'rgb(107, 107, 107)'
      }
    },
    paper_bgcolor:'rgba(0,0,0,0)',
    plot_bgcolor:'rgba(0,0,0,0)',
    
    width: two_sizes.sizew,
    height: two_sizes.sizeh,

    margin: {
      l: 60,
      r: 10,
      b: 30,
      t: 30,
      pad: 2
    },
  };
  
  Plotly.newPlot(barDiv, data, layout);
  barDiv.on('plotly_click', function(data){
    window.location.replace('/plot/clima/dashboard')
  });
}

function plotlyGroupUdate(container, source, start_date, end_date, rangeLabel, size){
  
  SOURCE_URL = setSource(source, start_date, end_date);
  var valuesX = []
  var acumulado = []
  var promedio = []
  var minimo = []
  var maximo = []

  groupBarDiv = document.getElementById(container);
  var colorScheme = ["#FF8A65", "#4DB6AC","#FFF176","#BA68C8","#00E676","#AED581","#9575CD","#7986CB","#E57373","#A1887F","#90A4AE","#64B5F6"];
  Plotly.d3.json(SOURCE_URL, function(error, data) {
        data.forEach(function(item){
              valuesX.push(item.categorie)
              acumulado.push(item.values[0].value)
              minimo.push(item.values[1].value)
              maximo.push(item.values[2].value)
              promedio.push(item.values[3].value)
        })


        var trace1 = {
          x: valuesX,
          y: acumulado,
          name: 'Acumulado',
          marker: {color: '#64B5F6'},
          type: 'bar'
        };
        
        var trace2 = {
          x: valuesX,
          y: minimo,
          name: 'Minimo',
          marker: {color: '#A1887F'},
          type: 'bar'
        };
        
        var trace3 = {
          x: valuesX,
          y: maximo,
          name: 'Maximo',
          marker: {color: 'rgb(26, 40 , 255)'},
          type: 'bar'
        };

                  
        var trace4 = {
          x: valuesX,
          y: promedio,
          name: 'Promedio',
          marker: {color: "#00E676"},
          type: 'bar'
        };

        var data_update = [trace1, trace2, trace3, trace4];
        var two_sizes = getGroupChartViewBox(getChartPluginSize(size));
        var layout_update = {
          title: '',
          xaxis: {
              title: 'years',
              tickfont: {
              size: 14,
              color: 'rgb(107, 107, 107)',
            }},
          yaxis: {
            title: rangeLabel,
            titlefont: {
              size: 16,
              color: 'rgb(107, 107, 107)'
            },
            tickfont: {
              size: 14,
              color: 'rgb(107, 107, 107)'
            }
          },

          barmode: 'group',
          bargap: 0.15,
          bargroupgap: 0.1,
          
          width: two_sizes.sizew,
          height: two_sizes.sizeh,

          margin: {
            l: 60,
            r: 50,
            b: 70,
            t: 15,
            pad: 2
          },
        };
        
        Plotly.newPlot(groupBarDiv, data_update, layout_update);  
        groupBarDiv.on('plotly_click', function(data){
          window.location.replace('/plot/clima/dashboard')
        });
      });
}


function changeGroupedOnDate(id_first_date,id_last_date, container, source,rangeLabel,size ){

  value = $("#"+id_first_date).val();
  value_new = $("#"+id_last_date).val()
  start_date = value == ""? null: new Date(value).toISOString().slice(0,10) 
  end_date = value_new == "" ? null : new Date(value_new).toISOString().slice(0,10)   
  if(start_date!==null && end_date!==null){
    plotlyGroupUdate(container, source, start_date, end_date, rangeLabel, size)
  }
}

