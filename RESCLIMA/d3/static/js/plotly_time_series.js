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
	if (size == 4) { return { sizew : 320, sizeh : 220} }
	else if (size == 5) { return { sizew : 385, sizeh : 290} }
	else if (size == 6) { return { sizew : 470, sizeh : 360} }
	else { return { sizew : 560,  sizeh : 440} }
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
    if (!checkDate(start_date, end_date)) {
      // Una de las fechas ingresadas no es valida
      start_date = null;
      end_date = null;
    }
    
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
  