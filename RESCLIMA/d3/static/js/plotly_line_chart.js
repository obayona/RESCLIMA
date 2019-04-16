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

function getLineChartViewBox(size) {
  console.log(1)
	if (size == 4) { return { sizew : 320, sizeh : 200} }
	else if (size == 5) { return { sizew : 400, sizeh : 280} }
	else if (size == 6) { return { sizew : 500, sizeh : 310} }
	else { return { sizew : 520,  sizeh : 350} }
}

function setLegend(str) {
    if (str.includes("W")) {return "Pesados"} 
    else if (str.includes("L")) {return "Livianos"} 
    else {return "Undefined"}
  }

function setSource(sid, source, start_date, end_date) {
	if (!sid) { return "http://127.0.0.1:8000/api/" + source + "/" + start_date + "/" + end_date + "/"; }
	else { return "http://127.0.0.1:8000/api/" + source + "/" + sid; }
}

function setOrigin(sid, origin, start_date, end_date) {
	if (!sid) { return "http://127.0.0.1:8000/api/" + origin + "/" + start_date + "/" + end_date + "/"; }
	else { return "http://127.0.0.1:8000/api/" + origin + "/" + sid; }
}

function isEmpty(str) {
	if (!str) { return true; }
	else { return false }
}

function checkDate(start_date, end_date) {
    if (!isEmpty(start_date) && !isEmpty(end_date)) { return true; }
   else { return false; }
 }

 /**Funcion que genera stack charts que pueden transformarse en line charts segun un evento
  * de click, falta agregar funcionalidad de cambio y funcionalidad de conexion entre series de tiempo
  * 
  */
function plotlyLineChart(container, start_date, end_date, source, origin, domainLabel, rangeLabel, size, sid, color, hover) {
    if (!checkDate(start_date, end_date)) {
      // Una de las fechas ingresadas no es valida
      start_date = null;
      end_date = null;
    }
    SOURCE_URL = setSource(sid, source, start_date, end_date);
    ORIGIN_URL = setOrigin(sid, origin, start_date, end_date);
    var myDiv = document.getElementById(container);
    var sourx = []
    var soury = []
    var origx = []
    var origy = []

    d3.queue()
        .defer(Plotly.d3.json, SOURCE_URL)
        .defer(Plotly.d3.json, ORIGIN_URL)
        .await(function(error,data, data2){
            if(error){
                console.error(error);
            }else{
                data.forEach(function(item){
                    sourx.push(item.key)
                    soury.push(item.value)
                })
                data2.forEach(function(item){
                    origx.push(item.key)
                    origy.push(item.value)
                })
                var trace1 = {
//                    name : domainLabel,
                    x: sourx,
                    y: soury,
                    fill: 'tozeroy',
                    type: 'scatter',
                    mode: 'none',
                    fillcolor : color,
                    name : setLegend(source)
                  };
                  
                  var trace2 = {
//                    name : origin,
                    x: origx,
                    y: origy,
                    fill: 'tonexty',
                    type: 'scatter',
                    mode: 'none',
                    fillcolor: hover,
                    name : setLegend(origin)
                  };
                  var two_sizes = getLineChartViewBox(getChartPluginSize(size));
                  var layout = {
                    xaxis: {
                      title: domainLabel,
                    },
                    yaxis: {
                      title: rangeLabel,
                      zeroline: false,
                    },
                    width: two_sizes.sizew,
                    height: two_sizes.sizeh,    
                    margin: {
                        l: 40,
                        r: 10,
                        b: 30,
                        t: 30,
                        pad: 2
                      },
                  };
                  
                  var data = [trace1, trace2];
                  
                  Plotly.newPlot(myDiv, data, layout);
            }
        })
}

function plotly_ALF_line_chart(container, start_date, end_date, source, domainLabel="años", rangeLabel="Personas", size, sid){

  SOURCE_URL = setSource(sid, source, start_date, end_date);
  var myDiv = document.getElementById(container);
  years = []
  llettered = []
  lunlettered = []

  Plotly.d3.json(SOURCE_URL, function(error, data) {
    data.forEach(function(item){
          llettered.push(item.value.lettered)
          lunlettered.push(item.value.unlettered)
          years.push(item.key)
      });
      var trace1 = {
        //          name : domainLabel,
        x: years,
        y: llettered,
        fill: 'tozeroy',
        type: 'scatter',
        mode: 'none',
        fillcolor : "#BA68C8",
        name : "letrado"
      };
      
      var trace2 = {
        //          name : origin,
        x: years,
        y: lunlettered,
        fill: 'tonexty',
        type: 'scatter',
        mode: 'none',
        fillcolor: "#9575CD",
        name : 'iletrado'
      };
      var two_sizes = getLineChartViewBox(getChartPluginSize(size));
      var layout = {
        xaxis: {
          title: domainLabel,
        },
        yaxis: {
          title: rangeLabel,
          zeroline: false,
        },
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
      
      var data = [trace1, trace2];
      
      Plotly.newPlot(myDiv, data, layout);
      
  })

}


function plotly_Housing_line_chart(container, start_date, end_date, source, domainLabel="años", rangeLabel="Viviendas", size, sid){
  SOURCE_URL = setSource(sid, source, start_date, end_date);
  var myDiv = document.getElementById(container);
  years = []
  lhousing = []

  Plotly.d3.json(SOURCE_URL, function(error, data) {
    data.forEach(function(item){
          lhousing.push(item.value.housing)
          years.push(item.key)
      });
      var trace1 = {
        //          name : domainLabel,
        x: years,
        y: lhousing,
        fill: 'tozeroy',
        type: 'scatter',
        mode: 'none',
        fillcolor : "#BA68C8",
        name : "viviendas"
      };
      

      var two_sizes = getLineChartViewBox(getChartPluginSize(size));
      var layout = {
        xaxis: {
          title: domainLabel,
        },
        yaxis: {
          title: rangeLabel,
          zeroline: false,
        },
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
      
      var data = [trace1];
      
      Plotly.newPlot(myDiv, data, layout);
      
  })
}