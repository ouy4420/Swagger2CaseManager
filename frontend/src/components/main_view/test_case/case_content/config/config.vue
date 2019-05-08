<template>

  <div>
    <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
      <el-tab-pane label="用例描述" name="name">
        <case_name></case_name>
      </el-tab-pane>
      <el-tab-pane label="参数驱动" name="parameters">
        <parameters></parameters>
      </el-tab-pane>
      <!--<el-tab-pane label="请求参数" name="request">-->

      <!--</el-tab-pane>-->
      <el-tab-pane label="全局变量" name="variables">
        <variables_global></variables_global>
      </el-tab-pane>
    </el-tabs>
  </div>

</template>

<script>
  import VariablesGlobal from './variables/variables_global'
  import Parameters from './parameters/parameters'
  import CaseName from './case_name/case_name'

  export default {
    name: "Config",
    components: {
      "case_name": CaseName,
      "variables_global": VariablesGlobal,
      "parameters": Parameters
    },
    data() {
      return {
        activeName: 'name',
      }
    },
    methods: {
      handleClick(tab, event) {
        console.log(1, tab);
        console.log(2, event);
      },

    },
    mounted() {

    }
  }
</script>

<style scoped>

</style>
