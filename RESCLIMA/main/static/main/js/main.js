// Router
const router = new VueRouter({
  mode: 'history'
})

// app principal
var app = new Vue({
	router,
	el:'#searchForm',
	delimiters: ['[[', ']]'],

	data:{
		shared:store // referencia al store de datos global
	},
	computed: {
		show_text: function(){
			var output_text = this.shared.text + " "

			var categories_text = ""
			var categories = this.shared.categories
			for(i=0; i< categories.length;i++){
				var cat = categories[i]
				if(cat.selected){
					cat = cat.name + " "
					categories_text += cat
				}
			}
			if(categories_text.length > 1){
				output_text += " - Categorias: "+categories_text
			}
			if (output_text.length>60){
				return output_text.slice(0,57) + "..."
			}
			return output_text
		},
		show_bbox: function(){
			var bbox = this.shared.bbox
			//minX: -87.37671375274657, minY: -24.805571117597832, maxX: -51.86890125274668, maxY: 4.960833531501636,
			if(bbox && bbox["minX"] && bbox["minY"] && bbox["maxX"] && bbox["maxY"]){
				var output_text = "[minX: ?1, minY: ?2, maxX: ?3, maxY: ?4]"
				output_text=output_text.replace("?1",bbox["minX"].toFixed(2))
				output_text=output_text.replace("?2",bbox["minY"].toFixed(2))
				output_text=output_text.replace("?3",bbox["maxX"].toFixed(2))
				output_text=output_text.replace("?4",bbox["maxY"].toFixed(2))
				return output_text
			}
			return ""
		},
		show_dates: function(){
			var ini_date = this.shared.ini_date
			var end_date = this.shared.end_date

			if(!ini_date && !end_date)
				return ""

			var output_text = "?1 : ?2"
			if(ini_date)
				output_text = output_text.replace("?1",ini_date)
			else
				output_text = output_text.replace("?1","")
			if(end_date)
				output_text = output_text.replace("?2",end_date)
			else
				output_text = output_text.replace("?2","")

			return output_text
		},
		show_option: function(){
			var option = this.shared.search_option
			if(option=="series")
				return "Series de tiempo"
			if(option=="layers")
				return "Capas"
			return ""
		}
	},
	methods:{
		// cuando se da click en el boton buscar
		// se ejecuta este metodo
		// search(), realiza una peticion post para
		// buscar los resultados (capas o series de tiempo)
		search:function(){
			var option = this.shared.search_option;
			if(option == "layers"){
				this.$root.$emit('searchLayers');
			}
			if(option == "series"){
				this.$root.$emit('searchSeries');
			}
		},

		
	}

})


