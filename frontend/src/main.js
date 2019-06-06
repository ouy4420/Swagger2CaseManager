import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App'
import router from './router'
// import './assets/styles/iconfont.css'
import * as api from './restful/api'
import store from './store'

Vue.config.productionTip = false;
Vue.use(ElementUI);
Vue.prototype.$api = api;

Vue.prototype.setLocalValue = function (name, value) {
  if (window.localStorage) {
    localStorage.setItem(name, value);
  } else {
    alert('This browser does NOT support localStorage');
  }
};
Vue.prototype.getLocalValue = function (name) {
  const value = localStorage.getItem(name);
  if (value) {
    return value;
  } else {
    return '';
  }
};

Vue.prototype.fail_notify = function (resp) {
  this.$alert(resp["msg"], '温馨提示：', {
    confirmButtonText: '确定',
    callback: action => {

    }
  });
};

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: {App},
  template: '<App/>',
  // 重新刷新页面后，App的store会被重置
  // 解决办法：利用浏览器的缓存
  // 还有避免页面get 304的问题？！
  created() {
    if (this.getLocalValue("routerName") === null) {
      this.setLocalValue("routerName", "ProjectList");
    }

    this.$store.commit("isLogin", this.getLocalValue("token"));
    this.$store.commit("setUser", this.getLocalValue("user"));
    this.$store.commit("setRouterName", this.getLocalValue("routerName"))

  }
});

