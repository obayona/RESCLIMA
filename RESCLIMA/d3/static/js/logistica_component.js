Vue.component("poblacion_component",{

    template:
    `
    <div class='row'>
        <div class="card">
          <div class="card-content">
            <p>Informacion adquirida sobre poblacion</p>
          </div>
          <div class="card-tabs">
            <ul class="tabs tabs-fixed-width">
              <li class="tab"><a href="#test4log">Test 1</a></li>
              <li class="tab"><a class="active" href="#test5log">Test 2</a></li>
              <li class="tab"><a href="#test6log">Test 3</a></li>
            </ul>
          </div>
          <div class="card-content grey lighten-4">
            <div id="test4log">
                <div class="row">
                    <div class="col 5">
                    </div>
                    <div class="col 7" id="pobInit">
                    </div>
                </div>

            </div>
            <div id="test5log">
                <div class="row">
                    <div class="col 5">
                    </div>
                    <div class="col 7" id="pobInit">
                    </div>
                </div>
            </div>
            <div id="test6log">
                <div class="row">
                    <div class="col 5">
                    </div>
                    <div class="col 7" id="pobInit">
                    </div>
                </div>            
            </div>
          </div>
        </div>
    </div>
    `,
    data(){
		return {
			selected_count:0,
			state:'initial',
			// limit y offset controlan la paginacion
			limit:4,
			offset:0,
			// maximo offset, al principio
			// se tiene un valor negativo
			max_offset:-1,
			shared:store
		}
    },
	mounted(){
		this.$root.$on('searchSeries', this.searchSeries);
    },
    methods:{
        
    }
})