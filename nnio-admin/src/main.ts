import Vue from 'vue';
import App from './App.vue';
import router from './router';
import axios from 'axios';
import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

// Vue.config.productionTip = false;
Vue.use(BootstrapVue);

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');

axios.interceptors.request.use(request => {
  const jwt = localStorage.getItem('jwt');
  if (jwt) {
    request.headers['Authorization'] = "Bearer " + jwt;
  }
  return request;
});

