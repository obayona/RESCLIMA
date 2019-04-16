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

function setSource(sid, source, start_date, end_date) {
	if (!sid) { return "http://127.0.0.1:8000/api/" + source + "/" + start_date + "/" + end_date + "/"; }
	else { return "http://127.0.0.1:8000/api/" + source + "/" + sid; }
}


function plotlyBarChartSample(container, source, start_date, end_date, domainLabel, rangeLabel, color, hover, sid, size){
    if (!checkDate(start_date, end_date)) {
        // Una de las fechas ingresadas no es valida
        start_date = null;
        end_date = null;
      }
      var barDiv = document.getElementById(container);
       // Check source
     SOURCE_URL = setSource(sid, source, start_date, end_date);
      var valuesX = []
      var valuesY = []

      d3.json(SOURCE_URL, function(error, data) {
        data.forEach(function(item){
              item.enabled = true;
              valuesX.push(item.value)
              valuesY.push(item.key)
        })
        console.log(valuesX)
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

        Plotly.newPlot(barDiv, data,layout);

        })
}

function change_to_stack(trace, bardiv){

}















