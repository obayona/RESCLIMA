// Router
const router = new VueRouter({
    mode: 'history'
  })
  
  // app principal
  var app = new Vue({
      router,
      el:'#trackingApp',
      data:{
          shared:store
      }
  })