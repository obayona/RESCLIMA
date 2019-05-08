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

function getBarChartViewBox(size) {
	if (size == 4) { return { sizew : 300, sizeh : 210} }
	else if (size == 5) { return { sizew : 400, sizeh : 280} }
	else if (size == 6) { return { sizew : 500, sizeh : 310} }
	else { return { sizew : 500,  sizeh : 400} }
}

function isEmpty(str) {
	if (!str) { return true; }
	else { return false }
}

function checkDate(start_date, end_date) {
   if (!isEmpty(start_date) && !isEmpty(end_date)) { return true; }
  else { return false; }
}

function setBarSource(sid, source, start_date, end_date) {
	if (!sid) { return "/api/" + source + "/" + start_date + "/" + end_date + "/"; }
	else { return "/api/" + source + "/" + sid; }
}


function plotlyBarChartSample(container, source, start_date, end_date, domainLabel, rangeLabel, color, hover, sid, size){
    if (!checkDate(start_date, end_date)) {
        // Una de las fechas ingresadas no es valida
        start_date = null;
        end_date = null;
      }
      var barDiv = document.getElementById(container);
       // Check source
     SOURCE_URL = setBarSource(sid, source, start_date, end_date);
      var valuesX = []
      var valuesY = []

      d3.json(SOURCE_URL, function(error, data) {
        data.forEach(function(item){
              item.enabled = true;
              valuesX.push(item.value)
              valuesY.push(item.key)
        })

        var trace1 = {
            x: valuesX,
            y: valuesY,
            type: 'bar',
            marker: {
              color: color,
            },
            source:source,
        };

            var data = [trace1];
            var two_sizes = getBarChartViewBox(getChartPluginSize(size));
            
            var layout = {
              font:{
                family: 'Raleway, sans-serif',
                color: hover,
              },
              showlegend: false,
              xaxis: {
                zeroline : true,
                title: domainLabel,
                tickangle: 0
              },
              yaxis: {
                title: rangeLabel,
                zeroline: true,
                gridwidth: 2
              },
              bargap :0.05,
                width: two_sizes.sizew,
                height: two_sizes.sizeh,

                margin: {
                  l: 40,
                  r: 20,
                  b: 30,
                  t: 20,
                  pad: 2
                },
            };

        Plotly.newPlot(barDiv, data,layout);

        barDiv.on('plotly_click', function(data){
          var selected_path = data
          //applyInteractivity(source,selected_path)
          redirect(selected_path.points[0].data.source)
        });

        })
}

function plotlyUpdateChart(container, source, start_date, end_date, domainLabel, rangeLabel, color, hover, sid, size){
  var barDiv = document.getElementById(container);
  // Check source
SOURCE_URL = setBarSource(sid, source, start_date, end_date);
 var valuesX = []
 var valuesY = []

 d3.json(SOURCE_URL, function(error, data) {
   data.forEach(function(item){
         item.enabled = true;
         valuesX.push(item.value)
         valuesY.push(item.key)
   })

   var trace1 = {
       x: valuesX,
       y: valuesY,
       type: 'bar',
       marker: {
         color: color,
       }
   };

       var data = [trace1];
       var two_sizes = getBarChartViewBox(getChartPluginSize(size));
       
       var layout = {
         font:{
           family: 'Raleway, sans-serif',
           color: hover,
         },
         showlegend: false,
         xaxis: {
           zeroline : true,
           title: domainLabel,
           tickangle: 0
         },
         yaxis: {
           title: rangeLabel,
           zeroline: true,
           gridwidth: 2
         },
         bargap :0.05,
           width: two_sizes.sizew,
           height: two_sizes.sizeh,

           margin: {
             l: 40,
             r: 20,
             b: 30,
             t: 20,
             pad: 2
           },
       };

   Plotly.update(barDiv, data,layout);

   })
}

function changeBarOnDate(id_first_date,id_last_date, container, source,domainLabel, rangeLabel, color, hover, sid, size){

  value = $("#"+id_first_date).val();
  value_new = $("#"+id_last_date).val()
  start_date = value == ""? null: new Date(value).toISOString().slice(0,10) 
  end_date = value_new == "" ? null : new Date(value_new).toISOString().slice(0,10)   
  if(start_date!==null && end_date!==null){
    plotlyBarChartSample(container, source, start_date, end_date, domainLabel, rangeLabel, color, hover, sid, size)
  }
}

function redirect(source){
  var logistica = ['LMS','EN','NO','ON','OE','NE','logistica']
  var clima = ['measurement','oni','rr','tmean','tmax','tmin','grouped']
  var poblacion = ['censo','population','alf']

  logistica.forEach(function(item){
    if(source.endsWith(item)){
      window.location.replace("/plot/logistica/dashboard/");
    }
  })
  clima.forEach(function(item){
    if(source.endsWith(item)){
      window.location.replace('/plot/clima/dashboard')
    }
  })
  poblacion.forEach(function(item){
    if(source.endsWith(item)){
      window.location.replace('/plot/poblacion/dashboard')
    }
  })
}













