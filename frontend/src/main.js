// // The Vue build version to load with the `import` command
// // (runtime-only or standalone) has been set in webpack.base.conf with an alias.
//
//
// // main.js 作为入口文件
// import Vue from 'vue'         // 用于创建ViewModel
// import App from './App'       // main.js中引用App.vue(作为根组件)，根组件又包含各种子孙组件
// import router from './router' /*
//                                  main.js中引用router中的index.js中export的Router实例
//                                  （ctrl+b 就能知道router是router中的index.js中export出的值，其他同理！
//                                  这个实例中包含了所有组件的路由情况
//                               */
// import ElementUI from 'element-ui';
// import 'element-ui/lib/theme-chalk/index.css';
//
// Vue.use(ElementUI);
// import * as api from './restful/api'
// import store from './store'
//
// Vue.prototype.$api = api;
// Vue.config.productionTip = false;
// Vue.filter('datetimeFormat', function (time, format = 'YY-MM-DD hh:mm:ss') {
//     let date = new Date(time);
//     let year = date.getFullYear(),
//         month = date.getMonth() + 1,
//         day = date.getDate(),
//         hour = date.getHours(),
//         min = date.getMinutes(),
//         sec = date.getSeconds();
//     let preArr = Array.apply(null, Array(10)).map(function (elem, index) {
//         return '0' + index;
//     });
//
//     let newTime = format.replace(/YY/g, year)
//         .replace(/MM/g, preArr[month] || month)
//         .replace(/DD/g, preArr[day] || day)
//         .replace(/hh/g, preArr[hour] || hour)
//         .replace(/mm/g, preArr[min] || min)
//         .replace(/ss/g, preArr[sec] || sec);
//
//     return newTime;
// });
// Vue.filter("timestampToTime", function (timestamp) {
//     let date = new Date(timestamp * 1000);
//     const Y = date.getFullYear() + '-';
//     const M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1) + '-';
//     const D = date.getDate() + ' ';
//     const h = date.getHours() + ':';
//     const m = date.getMinutes() + ':';
//     const s = date.getSeconds();
//
//     return Y + M + D + h + m + s;
//
// });
// Vue.prototype.setLocalValue = function (name, value) {
//     if (window.localStorage) {
//         localStorage.setItem(name, value);
//     } else {
//         alert('This browser does NOT support localStorage');
//     }
// };
// Vue.prototype.getLocalValue = function (name) {
//     const value = localStorage.getItem(name);
//     if (value) {
//         return value;
//     } else {
//         return '';
//     }
// };
// router.beforeEach((to, from, next) => {
//     console.log("to", to)
//     console.log("from", from)
//     console.log("next", next)
//     /* 路由发生变化修改页面title */
//     setTimeout((res) => {
//         if (to.meta.title) {
//             document.title = to.meta.title
//         }
//
//         if (to.meta.requireAuth) {
//             if (store.state.token !== '') {
//                 next();
//             } else {
//                 next({
//                     name: 'Login',
//                 })
//             }
//         } else {
//             next()
//         }
//     })
//
// });
//
//
// /* eslint-disable no-new */
// new Vue({
//     el: '#app',
//     router,
//     components: {App},
//     template: '<App/>',
//     store,
//     created() {
//         if (this.getLocalValue("token") === null) {
//             this.setLocalValue("token", "");
//         }
//         if (this.getLocalValue("user") === null) {
//             this.setLocalValue("user", "");
//         }
//         if (this.getLocalValue("routerName") === null) {
//             this.setLocalValue("routerName", "ProjectList");
//         }
//         this.$store.commit("isLogin", this.getLocalValue("token"));
//         this.$store.commit("setUser", this.getLocalValue("user"));
//         this.$store.commit("setRouterName", this.getLocalValue("routerName"));
//
//     }
// });


// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App'
import router from './router'
import './assets/styles/iconfont.css'
import './assets/styles/swagger.css'
import './assets/styles/tree.css'
import './assets/styles/home.css'
import './assets/styles/reports.css'
import * as api from './restful/api'
import store from './store'

Vue.config.productionTip = false;
Vue.use(ElementUI);
Vue.prototype.$api = api;

Vue.filter('datetimeFormat', function (time, format = 'YY-MM-DD hh:mm:ss') {
  let date = new Date(time);
  let year = date.getFullYear(),
    month = date.getMonth() + 1,
    day = date.getDate(),
    hour = date.getHours(),
    min = date.getMinutes(),
    sec = date.getSeconds();
  let preArr = Array.apply(null, Array(10)).map(function (elem, index) {
    return '0' + index;
  });

  let newTime = format.replace(/YY/g, year)
    .replace(/MM/g, preArr[month] || month)
    .replace(/DD/g, preArr[day] || day)
    .replace(/hh/g, preArr[hour] || hour)
    .replace(/mm/g, preArr[min] || min)
    .replace(/ss/g, preArr[sec] || sec);

  return newTime;
});

Vue.filter("timestampToTime", function (timestamp) {
  let date = new Date(timestamp * 1000);
  const Y = date.getFullYear() + '-';
  const M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1) + '-';
  const D = date.getDate() + ' ';
  const h = date.getHours() + ':';
  const m = date.getMinutes() + ':';
  const s = date.getSeconds();

  return Y + M + D + h + m + s;

});

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

