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
		// buscar(), realiza una peticion post para
		// buscar los resultados (capas o series de tiempo)
		buscar:function(){
			var data = this.shared.getPostData()
			console.log("Esto se busca",data)
			if(data==null){
				console.log("Error: debe haber al menos un parametro");
				return;
			}
			var url = null;
			if(this.shared.search_option == "layers"){
				url = "search/layers/";
			}
			if(this.shared.search_option == "series"){
				url = "search/series/";
			}
			var request = $.post(url,data);
			request.done(function(response){
				console.log("la respuesta",response);
				var results = store.results;
				var  results_response= response["results"];
				results.splice(0, results.length);
				for (var i=0;i< results_response.length; i++){
					results.push(results_response[i]);
				}
			});
			request.progress(function(error){
				console.log("Cargando resultados...");
			});
			request.fail(function(error){
				console.log(error);
			});
		}
	}

})

