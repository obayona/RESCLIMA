// ******************************************************************
// ************************* Simple function ************************
// ******************************************************************

function getChartPluginSize(str) {
    return parseInt(str[str.length-1]);
  }
  
  function getTimeChartViewBox(size) {
	if (size == 4) { return { sizew : 320, sizeh : 220} }
	else if (size == 5) { return { sizew : 385, sizeh : 290} }
	else if (size == 6) { return { sizew : 470, sizeh : 360} }
	else { return { sizew : 560,  sizeh : 440} }
  }
  
  function isEmpty(str) {
      if (!str) { return true; }
      else { return false }
  }
  
  function checkDate(start_date, end_date) {
     if (!isEmpty(start_date) && !isEmpty(end_date)) { return true; }
    else { return false; }
  }
  
  
  function plotlyTimeSeries(container, size, source, rangeLabel, start_date, end_date) {
    if (!checkDate(start_date, end_date)) {
      // Una de las fechas ingresadas no es valida
      start_date = null;
      end_date = null;
    }
    
    var datay = [],
        data_dates = [];
  
    // Define URL for JSON
    SOURCE_URL = " /api/" + source + "/" + start_date + "/" + end_date + "/";
    
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
  