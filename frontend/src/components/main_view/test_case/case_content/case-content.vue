<template>

  <div>
    <h1 class="title">Config(全局配置):</h1>
    <config style="margin-bottom: 40px"></config>
    <h1 class="title">Teststeps(测试步骤):</h1>
    <el-button size="medium" type="primary" @click="addStep" style="margin-bottom: 20px">
      <i class="el-icon-circle-plus"></i>AddStep
    </el-button>
    <teststeps></teststeps>
    <el-dialog
      title="添加TestStep"
      :visible.sync="DialogVisible"
      width="30%"
      align="center"
    >
      <!--<div v-for="api_name in apiList">{{api_name}}</div>-->
      <el-select v-model="api_name" placeholder="API模板">
        <el-option
          v-for="api in apiList"
          :key="api"
          :label="api"
          :value="api">
        </el-option>
      </el-select>

      <div slot="footer" class="dialog-footer">
        <el-button @click="DialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleConfirm()">确 定</el-button>
        <!--<el-button type="primary" @click="innerVisible = true">打开内层 Dialog</el-button>-->
      </div>
    </el-dialog>
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
      return {
        DialogVisible: false,
        api_name: null,
        apiList: [],
      }
    },
    methods: {
      addStep() {
        this.DialogVisible = true;
        const project_id = this.$route.params.id;
        this.$api.getAPIList({"id": project_id}).then(resp => {
            this.apiList = resp["api_list"];
          }
        )
      },
      handleConfirm() {
        var case_id = this.$store.state.currentCase.case_id;
        var api_name = this.api_name;
        var last_step_pos = this.$store.state.currentCase.last_step_pos + 1;
        var rquest_data = {
          "case_id": case_id,
          "api_name": api_name,
          "step_pos": last_step_pos
        };
        this.$api.addCase(rquest_data).then(resp => {
              if (resp['success']) {
              this.success(resp);       // 弹出成功提示消息
              this.get_case();          // 重新刷新当前case数据
            } else {
              this.failure(resp);
            }
          }
        );
        this. DialogVisible = false;

      },
      success(resp) {
        this.$notify({
          message: resp["msg"],
          type: 'success',
          duration: 1000
        });
      },
      failure(resp) {
        this.$notify.error({
          message: resp["msg"],
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
    mounted() {

    }
  }
</script>

<style scoped>
  .title {
    width: 100%;
    height: 10px;
    font-size: 30px;
    /*color: #fff;*/
    /*background: #1F5DEA;*/
    /*border: 1px solid #1F5DEA;*/
    /*border-radius: 2px;*/
  }
</style>
