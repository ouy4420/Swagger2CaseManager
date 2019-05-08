<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
  var App = {
    name: 'App',
    components: {}
  };
  export default App
</script>

<style>
  html, body {
    height: 100%;
    width: 100%;
    /*overflow: hidden;  */
    margin: 0;
    padding: 0;
    background: #fff;
  }

  body {
    color: #333;
    font-family: "PingFang SC", "Helvetica Neue", Helvetica, "Hiragino Sans GB", STHeitiSC-Light, "Microsoft YaHei", "微软雅黑", Arial, sans-serif
  }

  .el-notification {
    margin-top: 60px;
  }
  .el-message {
    margin-top: 60px;
  }
</style>
