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
      <el-form :model="stepForm"
               :rules="rules"
               label-width="110px"
               class="project"
               close>
        <el-form-item label="Step名称" prop="name">
          <el-input v-model="stepForm.name"></el-input>
        </el-form-item>
        <el-form-item label="API调用" prop="api_name">
          <el-select style="width: 425px" v-model="stepForm.api_name" placeholder="选择API调用">
            <el-option
              v-for="api in apiList"
              :key="api"
              :label="api"
              :value="api">
            </el-option>
          </el-select>
        </el-form-item>

      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="DialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleConfirm()">确 定</el-button>
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
        stepForm: {
          name: "",
          api_name: ""
        },
        rules: {
          name: [
            {required: true, message: '请输入Step名称', trigger: 'blur'},
            {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
          ]
        }
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
        if (this.stepForm.name === "") {
          this.$alert('请填写Step名称', '提示', {
            confirmButtonText: '确定',
            callback: action => {

            }
          });
          return
        }
        if (this.stepForm.api_name === "") {
          this.$alert('请选择API调用', '提示', {
            confirmButtonText: '确定',
            callback: action => {

            }
          });
          return
        }
        var case_id = this.$store.state.currentCase.case_id;
        var step_pos = this.$store.state.currentCase.last_step_pos + 1;
        var rquest_data = {
          "case_id": case_id,
          "name": this.stepForm.name,
          "api_name": this.stepForm.api_name,
          "step_pos": step_pos
        };
        this.$api.addStep(rquest_data).then(resp => {
            if (resp['success']) {
              this.success(resp);       // 弹出成功提示消息
              this.get_case();          // 重新刷新当前case数据
            } else {
              this.failure(resp);
            }
          }
        );
        this.stepForm = {
          name: "",
          api_name: ""
        };
        this.DialogVisible = false;

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
