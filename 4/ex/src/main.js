// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'

import axios from 'axios'

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
// 安装 ElementUI（ui）
Vue.use(ElementUI)

import App from './App'
import router from './router'

// 滚动条
import vuescroll from "vuescroll";//引入vuescroll
import "vuescroll/dist/vuescroll.css";//引入vuescroll样式
Vue.use(vuescroll);//使用

// echarts
const echarts = require('echarts');
Vue.prototype.$echarts = echarts

Vue.use(axios);
Vue.prototype.$axios = axios

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
