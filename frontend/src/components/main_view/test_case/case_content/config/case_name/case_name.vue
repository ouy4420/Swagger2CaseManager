<template>
  <div>
    {{this.$store.state.currentCase['config'].config.name}}
    <el-button type="text"
               icon="el-icon-edit"
               @click="editCaseName"
    ></el-button>
  </div>
</template>

<script>
  export default {
    methods: {
      editCaseName() {
        this.$prompt('请输入测试用例名称', '编辑用例名称', {
          inputValue: this.$store.state.currentCase['config'].config.name,
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          // inputPattern: /[^\u4e00-\u9fa5]+/,
          // inputErrorMessage: '请勿输入中文！！'
        }).then(({value}) => {
          // 提示成功消息
          this.$message({
            type: 'success',
            message: '新的用例名称是: ' + value
          });
          // 更新测试用例名称
          this.updateConfig(value);
          // 更新测试用例列表(注意：前一个动作也要访问数据库，避免冲突，此动作延时访问)
          var obj = this;
          function temp_func() {
            // obj.getPagination(1)
            obj.getCaseList()
          }
          setTimeout(temp_func, 500);
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消输入'
          });
        });
      },
      updateConfig(name) {
        var body = {
          "id": this.$store.state.currentCase['config'].config_id,
          "name": name
        };
        this.$api.updateConfigName(body).then(resp => {
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
      },
      getCaseList() {
        const project_id = this.$route.params.id;
        this.$api.getCaseList({"id": project_id}).then(resp => {
          this.$store.commit("setCaseList", resp["caseList"]);
        })
      }

    }
  }
</script>
