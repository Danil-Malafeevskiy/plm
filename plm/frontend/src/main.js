import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'


import VueLayers from 'vuelayers'
import 'vuelayers/dist/vuelayers.css'

Vue.config.productionTip = false
Vue.use(VueAxios, axios)
Vue.use(VueLayers)

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
