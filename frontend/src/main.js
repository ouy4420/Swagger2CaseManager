// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

// main.js 作为入口文件
import Vue from 'vue'         // 用于创建ViewModel
import App from './App'       // main.js中引用App.vue(作为根组件)，根组件又包含各种子孙组件
import router from './router' /*
                                 main.js中引用router中的index.js中export的Router实例
                                 （ctrl+b 就能知道router是router中的index.js中export出的值，其他同理！
                                 这个实例中包含了所有组件的路由情况
                              */

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: {App},
  template: '<App/>'
})
