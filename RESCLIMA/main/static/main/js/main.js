
var isEmpty = function(obj) {
    for (var prop in obj){
    	if (obj.hasOwnProperty(prop)){
    		return false;
    	}
    }
    return true;
};


var app = new Vue({
	el:'#searchForm',
	data:{
		textsearch:'',
		city:null,
		search_option:'Layers',
		currentComponent:"categories_component",
		shared: model
	},
	methods:{
		buscar:function(){
			var query = {}
			var model = this.shared
			if(this.textsearch!=''){
				query["text"]=this.textsearch;
			}
			if(model.ini_date && model.end_date){
				query["ini"]=model.ini_date
				query["end"]=model.end_date
			}
			if(model.bbox){
				query["bbox"]=model.bbox
			}
			var selectedCategories = []
			for(var i=0; i<model.categories.length; i++){
				var category = model.categories[i]
				if(category["selected"]){
					selectedCategories.push(category["id"])
				}
			}
			if(selectedCategories.length>0){
				query.categories = selectedCategories
			}
			if(isEmpty(query)){
				console.log("ERROR: seleccione algun parametro de busqueda")
				return
			}
			if(this.search_option=="Layers")
				console.log("Buscar capas",query)
			if(this.search_option=="Series")
				console.log("Buscar series de tiempo",query)
		}
	}

})
