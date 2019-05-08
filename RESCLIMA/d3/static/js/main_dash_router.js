// Router
const router = new VueRouter({
    mode: 'history'
  })
  
  // app principal
  var app = new Vue({
      router,
      el:'#mainViews',
      data:{
          shared:null // referencia al store de datos global
      },
      methods:{
          // cuando se da click en el boton buscar
          // se ejecuta este metodo
          // search(), realiza una peticion post para
          // buscar los resultados (capas o series de tiempo)

  
          
      }
  
  })