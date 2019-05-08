<template>

  <div>
    <div v-for="(item, index) in $store.state.currentCase['teststeps']">
      <span>TestStep{{index + 1}}:</span>
      <div>
        <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
          <el-tab-pane label="API描述" name="api_description">
            <step_name :stepItem="item"></step_name>
          </el-tab-pane>
          <el-tab-pane label="API调用" name="api_callfunction">
            <span>{{item.test.api}}</span>
          </el-tab-pane>
          <el-tab-pane label="局部变量" name="local_variables">
              <variables_local :stepItem="item"></variables_local>
          </el-tab-pane>
          <el-tab-pane label="断言校验" name="assert_validate">
            <validate v-bind:stepItem="item"></validate>
          </el-tab-pane>
          <el-tab-pane label="参数提取" name="params_extract">
            <extract v-bind:stepItem="item"></extract>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>

</template>

<script>
  import StepName from './step_name/step_name'
  import Vlidate from './validate/validate'
  import Extract from './extract/extract'
  import VariableLocal from './variables/variables_local'

  export default {
    name: "Teststeps",
    components: {
      "step_name": StepName,
      "validate": Vlidate,
      "extract": Extract,
      "variables_local": VariableLocal
    },
    data() {
      return {
        activeName: 'api_description',
        test_steps: null
      }
    },
    methods: {
      handleClick(tab, event) {
        // console.log(tab, event);
      }
    },
    created() {
      this.test_steps = this.$store.state.currentCase['teststeps']
    }
  }
</script>

<style scoped>

</style>




