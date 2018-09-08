Vue.component("categories_component",{
	template: `
		<div>
			<p>Puede seleccionar categorias
			para mejorar la b&uacute;squeda</p>

			<ul class="list-group">
			<li 
				v-for="category in shared.categories"
				class="list-group-item"
				v-bind:class="{active: category.selected}"
				v-on:click.prevent="category.selected=!category.selected">
				{{ category.name }} 		
			</ul>
		</div>
	`,

	data(){
		return {
			shared:model
		}
	}

})