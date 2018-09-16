const router = new VueRouter({
  mode: 'history'
})


var app = new Vue({
	router,
	el:'#searchForm',
	data:{
		city:null,
		currentComponent:"categories_component",
		shared:store
	},
	computed:{
		resultsList:function(){
			console.log(this.shared.search_option + "_component")
			return this.shared.search_option + "_component";
		}
	},
	methods:{
		buscar:function(){
			var data = this.shared.getPostData()
			console.log(data)
			if(data==null){
				console.log("Error: debe haber al menos un parametro")
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
				console.log(response);
				var results = store.results;
				var  results_response= response["results"];
				results.splice(0, results.length);
				for (var i=0;i< results_response.length; i++){
					results.push(results_response[i]);
				}
			});
			request.progress(function(error){
				console.log("Cargando resultados");
			});
			request.fail(function(error){
				console.log(error);
			});
		}
	}

})
