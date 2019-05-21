<template>
  <div>
    {{stepItem.test.name}}
    <el-button type="text"
               icon="el-icon-edit"
               @click="editAPIName"
    ></el-button>
  </div>
</template>

<script>
  export default {
    props: ["stepItem"],
    methods: {
      editAPIName() {
        this.$prompt('请输入API调用名称', '编辑API调用', {
          inputValue: this.stepItem.test.name,
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputPattern: /[^\u4e00-\u9fa5]+/,
          inputErrorMessage: '请勿输入中文！！'
        }).then(({value}) => {
          // 提示成功消息

          this.$message({
            type: 'success',
            message: '新的用例名称是: ' + value
          });
          // 更新测试API调用名称
          this.updateTestStep(value);
          console.log(this.stepItem)
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消输入'
          });
        });
      },
      updateTestStep(step_name) {
        var body = {
          "id": this.stepItem.step_id,
          "step_name": step_name
        };
        this.$api.updateStepAPIName(body).then(resp => {
          if (resp['success']) {
            this.success(resp);       // 弹出成功提示消息
            this.get_case();          // 重新刷新当前case数据
          } else {
            this.failure(resp);
          }
        })
      },
      success(resp) {
        this.$notify({
          message: resp["msg"],
          type: 'success',
          duration: 2000
        });
      },
      failure(resp) {
        this.$alert(resp["msg"], 'Error', {
          confirmButtonText: '确定',
          callback: action => {

          }
        });
        // this.$notify.error({
        //   message: resp["msg"],
        //   duration: 3000
        // });
      },
      get_case() {
        var currentCaseID = this.$store.state.currentCase['config'].case_id;
        this.$api.getCaseDetail(currentCaseID).then(resp => {
          this.$store.commit('setCurrentCase', resp);
        });
      }

    }
  }
</script>
