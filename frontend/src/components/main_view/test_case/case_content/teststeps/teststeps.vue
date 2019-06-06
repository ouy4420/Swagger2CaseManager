<template>

  <div>
    <div v-for="(item, index) in $store.state.currentCase['teststeps']" style="margin-bottom: 20px">
      <div style="margin-bottom: 5px">
        <el-button type="danger"
                   icon="el-icon-delete"
                   circle @click="delete_step(item.step_id)"
        >
         <!--v-if="index !== 0"-->
        </el-button>
        <span style="font-size: 25px">TestStep{{index + 1}}: {{item.test.api}}</span>
      </div>
      <div>
        <el-tabs v-model="item.step_pos" type="card" @tab-click="handleClick">
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
      return {}
    },
    methods: {
      delete_step(step_id) {
        // 弹出确认警告提示框
        this.$confirm('此操作将永久删除该TestStep, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$api.deleteStep({"step_id": step_id}).then(resp => {
            if (resp['success']) {
              this.success(resp);       // 弹出成功提示消息
              this.get_case();          // 重新刷新当前case数据
            } else {
              this.fail_notify(resp)
            }
          })
        })
      },
      handleClick(tab, event) {
        console.log(12345, tab, event);
      },
      success(resp) {
        this.$notify({
          message: resp["msg"],
          type: 'success',
          duration: 1000
        });
      },
      get_case() {
        var currentCaseID = this.$store.state.currentCase['config'].case_id;
        this.$api.getCaseDetail(currentCaseID).then(resp => {
          this.$store.commit('setCurrentCase', resp);
        });
      }
    },
    created() {

    }
  }
</script>

<style scoped>

</style>




