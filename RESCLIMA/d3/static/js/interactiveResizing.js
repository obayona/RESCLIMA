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

function getChartViewBox(size) {
	if (size == 4) { return { sizew : 320, sizeh : 220} }
	else if (size == 5) { return { sizew : 400, sizeh : 300} }
	else if (size == 6) { return { sizew : 500, sizeh : 330} }
	else { return { sizew : 520,  sizeh : 410} }
}

function setSource(sid, source, start_date, end_date) {
	if (!sid) { return " /api/" + source + "/" + start_date + "/" + end_date + "/"; }
	else { return " /api/" + source + "/" + sid; }
}

function setOrigin(sid, origin, start_date, end_date) {
	if (!sid) { return " /api/" + origin + "/" + start_date + "/" + end_date + "/"; }
	else { return " /api/" + origin + "/" + sid; }
}

function isEmpty(str) {
	if (!str) { return true; }
	else { return false }
}

function checkDate(start_date, end_date) {
    if (!isEmpty(start_date) && !isEmpty(end_date)) { return true; }
   else { return false; }
 }

/**Function that get the data series that are related to a determinated
 * Portion of a graph and renders a new graph of a different kind according
 * to the nature of the data
 */
function getDataInteraction(start_date, end_date, date_nature){

}


/**Function that returns an string according to a new type of graph that is going to be
 * return
 */
function setTypeOfNewGraph(){}

/**Function that renders a new graph according to the type of data obtained */
function renderNewGraph(){

}

/*************************************************************************
 ************************ LOGISTIC API MANAGEMENT ************************
 *************************************************************************/

var logisticAPIS = (source, start_date, end_date,sid) => {

	var endAPIS =  ['_L_EN', '_L_EO', '_L_NO', '_L_ON', '_L_OE', '_L_NE',
									'_W_EN', '_W_EO', '_W_NO', '_W_ON', '_W_OE', '_W_NE',
								]
	var sidAPIS = ['_WE', '_LE', '_WMS', '_LMS', '_WT', '_LT']
	

	if(!sid){
		var u =  " /api/" + source + "/" + start_date + "/" + end_date;
		var values = endAPIS.map(v => " /api/" + "_chart_"+source +v+ "/" + start_date + "/" + end_date )
	}else{
		var values = sidAPIS.map(v => " /api/" + "_chart_"+ source +v +"/" + sid )
	}
	return values;
}

function mainView(area, body){
	$('<div/>', {
    'id':'area',
    'class':'mainArea',
    'style':'cursor:pointer;font-weight:bold;',
    'html':'',
	}).appendTo(body);
}
function generateLogisticMainView(source, selectedPath){

	if(selectedPath=="Pesados"){
		//var str = str.includes("W")
	}else{}

}

function drawMain(element){
	var mainDiv = document.getElementById("id_main");
	mainDiv.appendChild(element)
}



/*************************************************************************
 ************************ CLIMATE API MANAGEMENT *************************
 *************************************************************************/



/*************************************************************************
 ************************** CENSUS API MANAGEMENT ************************
 *************************************************************************/