<template>

  <div>
    <h1 class="title">Config(全局配置):</h1>
    <config style="margin-bottom: 40px"></config>
    <h1 class="title">Teststeps(测试步骤):</h1>
    <teststeps></teststeps>
  </div>

</template>

<script>
  import Config from './config/config'
  import Teststeps from './teststeps/teststeps'

  export default {
    name: "CASEContent",
    components: {
      "config": Config,
      "teststeps": Teststeps
    },
    data() {
      return {}
    },
    methods: {},
    mounted() {

    }
  }
</script>

<style scoped>
  .title {
    width: 100%;
    height: 42px;
    font-size: 30px;
    /*color: #fff;*/
    /*background: #1F5DEA;*/
    /*border: 1px solid #1F5DEA;*/
    /*border-radius: 2px;*/
  }
</style>
