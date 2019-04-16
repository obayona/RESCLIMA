// ******************************************************************
// ************************* Simple function ************************
// ******************************************************************

function getChartPluginSize(str) {
    return parseInt(str[str.length-1]);
  }
  
  function getMultiChartViewBox(size) {
	if (size == 4) { return { sizew : 320, sizeh : 220} }
	else if (size == 5) { return { sizew : 400, sizeh : 290} }
	else if (size == 6) { return { sizew : 500, sizeh : 360} }
	else { return { sizew : 570,  sizeh : 440} }
  }

  
  function isEmpty(str) {
      if (!str) { return true; }
      else { return false }
  }
  
  function checkDate(start_date, end_date) {
     if (!isEmpty(start_date) && !isEmpty(end_date)) { return true; }
    else { return false; }
  }

  function define_Name(source){
    var comp = source.slice(-4);
    if(comp=='tmax') { return 'Máximo'}
    else if (comp=='tmin') {return "Mínimo"}
    else {return "Promedio"}
  }
  
  function plotlyMultiTimeSeries(container, size, source, origin, outset, rangeLabel, start_date, end_date) {
    if (!checkDate(start_date, end_date)) {
      // Una de las fechas ingresadas no es valida
      start_date = null;
      end_date = null;
    }
    SOURCE_URL = "http://127.0.0.1:8000/api/" + source + "/" + start_date + "/" + end_date + "/";
    ORIGIN_URL = "http://127.0.0.1:8000/api/" + origin + "/" + start_date + "/" + end_date + "/";
    OUTSET_URL = "http://127.0.0.1:8000/api/" + outset + "/" + start_date + "/" + end_date + "/";
    var barDiv = document.getElementById(container);

    var min_data = [],
        min_dates = [],
        max_data = [],
        max_dates = [],
        avg_data = [],
        avg_dates = [];

    d3.queue()
    .defer(d3.json, SOURCE_URL)
    .defer(d3.json, ORIGIN_URL)
    .defer(d3.json, OUTSET_URL)
    .await(function(error, dataset, dataset2, dataset3) {
        if (error) {
            console.error('Algo salió mal: ' + error);
        }
        else {
          dataset.forEach(function(item){
            min_data.push(item.count)
            min_dates.push(d3.time.format("%Y-%m-%d").parse(item.month))
        })
        dataset2.forEach(function(item){
          max_data.push(item.count)
          max_dates.push(d3.time.format("%Y-%m-%d").parse(item.month))
        })
        dataset3.forEach(function(item){
          avg_data.push(item.count)
          avg_dates.push(d3.time.format("%Y-%m-%d").parse(item.month))
        })
            var trace1 = {
                type: "scatter",
                mode: "lines",
                name: define_Name(source),
                x: min_dates,
                y: min_data,
                line: {color: '#17BECF'}
              }
              var trace2 = {
                type: "scatter",
                mode: "lines",
                name: define_Name(origin),
                x: max_dates,
                y: max_data,
                line: {color: '#7F7F7F'}
              }
              var trace3 = {
                type: "scatter",
                mode: "lines",
                name: define_Name(outset),
                x: avg_dates,
                y: avg_data,
                line: {color: '#7F1G7F'}
              }
              
              var data = [trace1,trace2, trace3];
              var two_sizes = getMultiChartViewBox(getChartPluginSize(size));
              var layout = {
                xaxis: {
                  autorange: true,
                  range: [min_dates[0], min_dates.slice(-1)[0] ],
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
        }
    })

  }