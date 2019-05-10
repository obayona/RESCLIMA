// ******************************************************************
// ************************* Simple function ************************
// ******************************************************************

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

/*************************************************************************
 ************************ CLIMATE API MANAGEMENT *************************
 *************************************************************************/



/*************************************************************************
 ************************** CENSUS API MANAGEMENT ************************
 *************************************************************************/