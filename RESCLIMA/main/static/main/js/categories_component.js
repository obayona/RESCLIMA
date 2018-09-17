var category_component = Vue.component("categories_component",{
	template: `
		<div>
			<p>Puede seleccionar categorias
			para mejorar la b&uacute;squeda</p>

			<div>
			     <div
				v-for="category in shared.categories"
				class="chip z-depth-3"
				v-bind:class="{cyan: category.selected}"
				v-on:click.prevent="selectCategory(category)">
				{{ category.name }}
			     </div>
			</div> 		
			</ul>
		</div>
	`,
	mounted(){
		var url = "search/categories/";
		var self = this;
		var categories_string = self.$route.query["categories"]
		var request = $.get(url);
		request.done(function(response){
			var categories = response.categories;
                        for(var i=0; i < categories.length; i++){
                                var category = categories[i];
                                self.shared.categories.push(category);
                        }
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
			shared:store
		}
	},
	methods:{
		selectCategory(category){
			category.selected = !category.selected
			var params = this.shared.getQueryParams()
			console.log("se reemplaza el url",params)
			this.$router.replace({query:params})
		}
	}
})

