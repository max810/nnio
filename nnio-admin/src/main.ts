import Vue from 'vue';
import App from './App.vue';
import router from './router';
import axios from 'axios';
import BootstrapVue from 'bootstrap-vue';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

axios.interceptors.request.use(request => {
  const jwt = localStorage.getItem('jwt');
  if (jwt) {
    request.headers['Authorization'] = "Bearer " + jwt;
  }
  return request;
});
Vue.filter('capitalize', function (value: any) {
  if (!value) return '';
  value = value.toString();
  return value.charAt(0).toUpperCase() + value.slice(1);
});
// Vue.config.productionTip = false;
Vue.use(BootstrapVue);

let vm = new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');

(<any>window).vm = vm;

console.log(vm);



