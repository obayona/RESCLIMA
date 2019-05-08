// ******************************************************************
// ************************* Simple function ************************
// ******************************************************************

function toTitleCase(str) {
    return str.replace(/\w\S*/g, function(txt){
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}

function isEmpty(str) {
	if (!str) { return true; }
	else { return false }
}

function getChartPluginSize(str) {
  return parseInt(str[str.length-1]);
}

function getChartViewBox(size) {
	if (size == 4) { return { sizew : 310, sizeh : 210} }
	else if (size == 5) { return { sizew : 370, sizeh : 285} }
	else if (size == 6) { return { sizew : 470, sizeh : 350} }
	else { return { sizew : 560,  sizeh : 440} }
}

function checkDate(start_date, end_date) {
   if (!isEmpty(start_date) && !isEmpty(end_date)) { return true; }
  else { return false; }
}

function getDivId(container, htmltag){
	var idtxt =  container.slice(6,container.length)
	return htmltag+"-"+idtxt;
}

function transform_back_to_tree(movements, livianos, pesados,values, barDiv,size){
	var shapes = [];
	var annotations = [];
	var counter = 0;
	// For Hover Text
	var x_trace = [];
	var y_trace = [];
	var text = [];

	//colors
	var colors = ['rgb(166,206,227)', 'rgb(31,120,180)', 'rgb(178,223,138)', 'rgb(51,160,44)', 'rgb(251,154,153)', 'rgb(227,26,28)', 'rgb(253,191,111)', 'rgb(255,127,0)', 'rgb(202,178,214)', 'rgb(106,61,154)', 'rgb(255,255,153)', 'rgb(177,89,40)'];

	// Generate Rectangles using Treemap-Squared
	var rectangles = Treemap.generate(movements, 100, 100);
	for (var i in rectangles) {
		var shape = {
								type: 'rect',
						x0: rectangles[i][0],
						y0: rectangles[i][1],
						x1: rectangles[i][2],
						y1: rectangles[i][3],
						line: {
								width: 1,
								color : "white",
							},
						fillcolor: colors[counter]
				};
		shapes.push(shape);
		var annotation = {
							x: (rectangles[i][0] + rectangles[i][2]) / 2,
							y: (rectangles[i][1] + rectangles[i][3]) / 2,
							text: String(values[counter]),
							showarrow: false,
							livianos:livianos[counter]
				};
		annotations.push(annotation);
			
		// For Hover Text
		x_trace.push((rectangles[i][0] + rectangles[i][2]) / 2);
		y_trace.push((rectangles[i][1] + rectangles[i][3]) / 2);
		text.push(String("livianos:"+livianos[counter]+"\n"+
		"pesados:"+pesados[counter]));
		pesados.push(pesados[counter])
		// Incrementing Counter		
		counter++;
	}

	// Generating Trace for Hover Text
	var trace0 = {
				x: x_trace,
				y: y_trace,
				text: text,
				mode: 'text',
				type: 'scatter',
				livianos: livianos,
				pesados: pesados,
			};
	var two_sizes = getChartViewBox(getChartPluginSize(size));
	
	var layout = {
				height: two_sizes.sizeh,
				width: two_sizes.sizew,
				margin: {
					l: 25,
					r: 10,
					b: 20,
					t: 20,
					pad: 2
				},
				shapes: shapes,
				paper_bgcolor: "rgba(0,0,0,0)",
				hovermode: 'closest',
				annotations: annotations,
				xaxis: {
							showgrid: false,
							zeroline: false
				},
				yaxis: {
							showgrid: false,
							zeroline: false
				}
	};

	var data = {
				data: [trace0]
	};
	Plotly.newPlot(barDiv, [trace0], layout);
	
	var no_clicked = true;

	barDiv.on('plotly_click', function(data){

		window.location.replace("/plot/logistica/dashboard/");
		if(no_clicked){
			index = data.points[0].pointIndex
			livianos_new = [livianos[index]]
			pesados_new = [pesados[index]]
			values_new = [values[index]]
			movements_new = [livianos_new+pesados_new]
			transform_back_to_tree(movements,livianos_new,pesados_new, values_new,barDiv,size)
		}
		else{
			transform_back_to_tree(movements,livianos,pesados, values,barDiv,size)
		}
		no_clicked=!no_clicked;
		})
}


function plotlyTreeMap(container, source, start_date, end_date, size) {
    if (!checkDate(start_date, end_date)) {
      // Una de las fechas ingresadas no es valida
      start_date = null;
      end_date = null;
    }
    SOURCE_URL = "/api/" + source + "/" + start_date + "/" + end_date + "/";
    var barDiv = document.getElementById(container);

    var movements = [],
        livianos = [],
        pesados = [],
        values = [];

    Plotly.d3.json(SOURCE_URL, function(error, data) {
      data.forEach(function(item){
            movements.push(item.values.livianos+item.values.pesados)
            livianos.push(item.values.livianos)
            pesados.push(item.values.pesados)
            values.push(item.values.sentido)
				})
				
			transform_back_to_tree(movements, livianos, pesados,values, barDiv,size)
			changeButton(movements, livianos, pesados,values,container,barDiv,size);
    })


}

function changeButton(movements, livianos, pesados,values,container,baseDiv,size){
	var barDiv = document.getElementById(getDivId(baseDiv.id,'i'));
	var treeDiv = document.getElementById(getDivId(baseDiv.id,"itree"));
	barDiv.addEventListener('click',function(){
		$("#"+container).empty();
		transform_to_bars(movements,livianos,pesados,values,baseDiv,size)
	})
	treeDiv.addEventListener('click', function(){
		$("#"+container).empty();
		transform_back_to_tree(movements,livianos,pesados,values,baseDiv,size)
	})

	
}

function transform_to_bars(movements, livianos, pesados,values, barDiv,size){

	var values = values.map(v => v.slice(7, v.length))

	var trace1 = {
		x: values,
		y: movements,
		name: 'totales',
		type: 'bar',
		text: values,
		marker: {
			color: 'rgb(142,124,195)'
		}
	};
	
	var trace2 = {
		x: values,
		y: livianos,
		type: 'bar',
		name: 'livianos',
		text: values,
		marker: {
			color: 'rgb(122,158,225)'
		}
	};

	var trace3 = {
		x: values,
		y: pesados,
		name:'pesados',
		type: 'bar',
		text: values,
		marker: {
			color: 'rgb(192,134,205)'
		}
	};

	var data = [trace1, trace2, trace3];
	var two_sizes = getChartViewBox(getChartPluginSize(size));
	
	var layout = {
		paper_bgcolor: "rgba(0,0,0,0)",
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
			title: 'sentidos'
		},
		yaxis: {
			zeroline: false,
			gridwidth: 2,
			title: "vehiculos"
		},
		bargap :0.05
	};

	Plotly.newPlot(barDiv,data,layout);
}



function changeMapedOnDate(id_first_date,id_last_date,container, source, size){
	value = $("#"+id_first_date).val();
	value_new = $("#"+id_last_date).val()
  start_date = value == ""? null: new Date(value).toISOString().slice(0,10) 
  end_date = value_new == "" ? null : new Date(value_new).toISOString().slice(0,10)   
	console.log(start_date)
	if(start_date!==null && end_date!==null){
		plotlyTreeMap(container, source, start_date, end_date, size)
	}
}

