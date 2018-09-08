Vue.component("time_component",{
	template: `
		<div>
			<p>Puede seleccionar un rango de fechas
			para los datos</p>
			<div>
		        <label for="Inicio">Inicio</label>
		        <input type="date" v-model="shared.ini_date"/>
		    </div>
    		<div>
        		<label for="Fin">Fin</label>
        		<input type="date" v-model="shared.end_date"/>
    		</div>
		</div>
	`,
	data(){
		return {
			shared: model
		}
	}
})