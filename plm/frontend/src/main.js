import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import store from './store'


//import VueLayers from 'vuelayers'
//import 'vuelayers/dist/vuelayers.css'

Vue.use(VueAxios, axios)
//Vue.use(VueLayers)
Vue.use(vuetify);


new Vue({
  router,
  vuetify,
  store,
  render: h => h(App)
}).$mount('#app')
