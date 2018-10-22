// Router
const router = new VueRouter({
  mode: 'history'
})

// app principal
var app = new Vue({
	router,
	el:'#searchForm',
	data:{
		city:null,
		currentComponent:"categories_component",
		shared:store // referencia al store de datos global
	},
	methods:{
		// cuando se da click en el boton buscar
		// se ejecuta este metodo
		// search(), realiza una peticion post para
		// buscar los resultados (capas o series de tiempo)
		search:function(){
			var data = this.shared.getPostData()
			console.log("Esto se busca",data)
			if(data==null){
				return;
			}
			var url = null;
			var option = this.shared.search_option;
			if(option == "layers"){
				url = "search/layers/";
			}
			if(option == "series"){
				url = "search/series/";
			}
			var request = $.post(url,data);
			request.done(function(response){
				var results = null;
				// dependiendo de la opcion
				// el resultado que envia el servidor
				// sera copiado en un arreglo adecuado
				if(option=="layers"){
					results = store.layers;
					store.layers_state = "searched"
				}
				if(option=="series"){
					results = store.series;
					store.series_state = "searched"
				}
				var  results_response= response["results"];
				results.splice(0, results.length);
				for (var i=0;i< results_response.length; i++){
					results.push(results_response[i]);
				}
			});
			request.progress(function(error){
				if(option=="layers"){
					store.layers_state = "loading";	
				}
				if(option=="series"){
					store.series_state = "loading";
				}
				
			});
			request.fail(function(error){
				if(option=="layers"){
					store.layers_state = "fail";	
				}
				if(option=="series"){
					store.series_state = "fail";
				}
			});
		},

		
	}

})


