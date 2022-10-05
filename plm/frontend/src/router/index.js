import Vue from 'vue'
import VueRouter from 'vue-router'
import ResetPasswordView from '@/views/ResetPasswordView.vue'

Vue.use(VueRouter)

const routes = [
    {
      path: '/reset-password/:id',
      name: 'reset-password',
      public: true,
      component: ResetPasswordView
    }
  ]

  const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
  })
  
  export default router