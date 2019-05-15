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

    .project_detail li {
    margin-top: 10px;
    text-indent: 20px;
    display: inline-block;
    height: 90px;
    width: calc(20% - 1.5px);
    border: 1px solid #ddd;
  }

  .title-project {
    margin-top: 20px;
    margin-left: 10px;
  }

  ul li {
    list-style: none;
  }

  .title-li {
    font-size: 44px;
    color: #607d8b;
  }

  .desc-li {
    margin-top: 30px;
    color: #b6b6b6;
    font-size: 14px;
  }
</style>
