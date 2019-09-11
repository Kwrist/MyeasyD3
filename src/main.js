import Vue from 'vue'
import * as d3 from 'd3'
import App from './App.vue'
import $ from 'jquery'
import axios from 'axios'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css';
import VueResource from 'vue-resource'

Vue.use(VueResource);
Vue.use(ElementUI);

Vue.prototype.$axios=axios;
Vue.prototype.$d3=d3;
window.d3=d3;
Vue.config.productionTip = false;


//渲染
new Vue({
  render: h => h(App),
}).$mount('#app1');
