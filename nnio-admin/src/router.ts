import Vue from 'vue';
import Router, { Location } from 'vue-router';
import Login from '@/views/Login.vue';
import Admin from '@/views/Admin.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/admin',
      name: 'admin',
      component: Admin,
      beforeEnter: (from, to, next) => {
        if (localStorage.getItem('jwt')) {
          return next();
        }

        return next({
          name: 'login',
          params: { 'msg': 'LOGIN FIRST MOTHERFUCKER!' }
        });
      },
    },
    {
      path: '/login',
      props: true,
      name: 'login',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: Login,
    },
  ],
});
