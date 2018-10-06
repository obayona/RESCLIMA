Vue.component("layers_component",{
	template: `
		<div id="layerList"
		v-bind:style="[open?{'left':'0px'}:{'left':'-220px'}]">
			<span><i class="material-icons">map</i>Capas</span>
			<div class="arrow" 
			 v-on:click.prevent="open=!open">
				<i v-if="open" class="material-icons">keyboard_arrow_left</i>
				<i v-else class="material-icons">keyboard_arrow_right</i>
			</div>
			<div>
			Lista de capas:
			</div>
		</div>			
	`,
	data(){
		return {
			open:true,
		}
	}
})

