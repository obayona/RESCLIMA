var category_component = Vue.component("categories_component",{
	template: `
		<div class="container">
			<div>
				<h4 style="text-align: center">Seleccione categor&iacute;as para mejorar la b&uacute;squeda</h4>
			</div>
			<br>
			<div class="container" style="text-align:center">
				<div
				v-for="category in shared.categories"
				class="chip z-depth-3"
				style="align-items: center; margin: 10px;"
				v-bind:class="{cyan: category.selected}"
				v-on:click.prevent="selectCategory(category)">
				{{ category.name }}
			     </div>
			</div> 		
			</ul>
		</div>
	`,
	mounted(){
		// se obtienen las categorias seleccionadas desde el url
		var categories_string = this.$route.query["categories"];
		// se obtienen las categorias desde el servidor
		var url = "search/categories/";
		var self = this;
		var request = $.get(url);
		request.done(function(response){
			var categories = response.categories;
			// setea las categorias traidas del servidor
			// en el store de datos global
			for(var i=0; i < categories.length; i++){
				var category = categories[i];
				self.shared.categories.push(category);
			}
			// si hay categorias seleccionadas, se las selecciona
			if(categories_string){
				selectedCategories = categories_string.split(",")
				for(var i=0; i< selectedCategories.length; i++){
					var idCategory = selectedCategories[i]
					for(var j=0; j < self.shared.categories.length; j++){
						var currentCat = self.shared.categories[j]
						if(currentCat["id"] == idCategory){
							currentCat["selected"] = true
						}
					}
				}
			}
		});
		request.fail(function(){
			console.log("Error fatal")
		});	
	},
	data(){
		return {
			shared:store // referencia al store global
		}
	},
	methods:{
		// se ejecuta cuando se da click en una categoria
		selectCategory(category){
			// se marca o desmarca la categoria
			category.selected = !category.selected
			// se actualiza el url
			var params = this.shared.getQueryParams()
			this.$router.replace({query:params})
		}
	}
})

