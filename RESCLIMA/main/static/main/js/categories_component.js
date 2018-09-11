Vue.component("categories_component",{
	template: `
		<div>
			<p>Puede seleccionar categorias
			para mejorar la b&uacute;squeda</p>

			<ul class="collection">
			<li 
				v-for="category in shared.categories"
				class="chip"
				v-bind:class="{active: category.selected}"
				v-on:click.prevent="category.selected=!category.selected">
				{{ category.name }} 		
			</ul>
		</div>
	`,
	mounted(){
		var url = "search/categories/";
		var self = this;
		var request = $.get(url);
		request.done(function(response){
			var categories = response.categories;
			for(var i=0; i < categories.length; i++){
				var category = categories[i];
				self.shared.categories.push(category);
			}
		});
		request.fail(function(){
			console.log("Error fatal")
		});	
	},
	data(){
		return {
			shared:model
		}
	}

})
