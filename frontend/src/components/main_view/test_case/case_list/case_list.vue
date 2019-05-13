<template>

  <div>
    <div style="padding: 10px; text-align: right; margin-bottom: 20px">
      <el-button type="success" round @click="runTest">执行测试</el-button>
    </div>
    <el-table
      @row-click="handleCurrentChange"
      @selection-change="selsChange"
      ref="multipleTable"
      :data="$store.state.caseList"
      tooltip-effect="dark"
      style="width: 100%"
    >
      <el-table-column
        type="selection"
        width="50">
      </el-table-column>
      <el-table-column
        prop="index"
        label="用例编号"
        width="100">
      </el-table-column>
      <el-table-column
        label="用例描述"
        width="280">
        <template slot-scope="scope">
          <a @click="setCaseItem(scope.row.id)">{{ scope.row.name }}</a>
        </template>
      </el-table-column>
    </el-table>
  </div>

</template>

<script>

  export default {
    name: "CASEList",
    data() {
      return {
        loading_flag: false,
        multipleSelection: [],
        page: {
          page_now: 1,
          page_previous: null,
          page_next: 2
        },
        arrID: []
      }
    },
    methods: {
      removeByValue(arr, val) {
        for (var i = 0; i < arr.length; i++) {
          if (arr[i] === val) {
            arr.splice(i, 1);
            break;
          }
        }
      },
      handleCurrentChange(row, event, column) {
        var same = false;
        if (this.arrID.length > 0) {
          for (var i = 0; i < this.arrID.length; i++) {
            if (this.arrID[i] === row.id) {
              same = true;
              this.removeByValue(this.arrID, row.id);
              break;
            }
          }
          if (same === true) {
            this.$refs.multipleTable.toggleRowSelection(row, false);
          } else {
            this.$refs.multipleTable.toggleRowSelection(row, true);
            this.arrID.push(row.id);
          }
        } else {
          this.$refs.multipleTable.toggleRowSelection(row, true);
          this.arrID.push(row.id);
        }
      },
      selsChange(val) {
        var valId = [];
        for (var i = 0; i < val.length; i++) {
          var arrIDsame = false;
          valId.push(val[i].id);
        }
        this.arrID = valId;
        console.log(this.arrID)
      },
      getPagination(page) {
        const project_id = this.$route.params.id;
        this.$api.getPagination_case({"id": project_id, "page": page}).then(resp => {
          this.caseList = resp["caseList"];
          this.page = resp["page"];
          this.setCaseItem(this.caseList[0].id);
        })

      },
      getCaseList() {
        const project_id = this.$route.params.id;
        this.$api.getCaseList({"id": project_id}).then(resp => {
          this.$store.commit("setCaseList", resp["caseList"]);
          this.setCaseItem(this.$store.state.caseList[0].id);
        })
      },
      setCaseItem(case_id) {
        this.$api.getCaseDetail(case_id).then(resp => {
          if (resp['success']) {
            this.$store.commit('setCurrentCase', resp);
            window.scrollTo(0, 0); // 滚动条弹到顶端
          } else {
            this.$notify.error({
              position: "top-left",
              message: resp["msg"],
              duration: 6000
            });
          }
          this.$refs.multipleTable.clearSelection(); // 清空checkbox所有选中
        });
      },
      runTest() {
        const project_id = this.$route.params.id;
        if (this.arrID.length === 0) {
          this.$notify.error({
            position: "top-left",
            message: "请选择要执行的测试用例！！！",
            duration: 3000
          });
          return
        }
        this.loading_flag = true;
        this.$emit('e-autotest', this.loading_flag);
        this.$api.runTestcases({"case_list": this.arrID, "project_id": project_id}).then(resp => {
          this.loading_flag = false;
          this.$emit('e-autotest', this.loading_flag);
          if (resp['success']) {
            var render_content = resp.render_content;
            this.success(resp);       // 弹出成功提示消息
            var newWin = window.open("", "_blank");
            newWin.document.write(render_content)
          } else {
            this.$notify.error({
              position: "top-left",
              message: resp["msg"],
              duration: 6000
            });
          }
        });
      },
      success(resp) {
        this.$notify({
          message: resp["msg"],
          type: 'success',
          duration: 2000
        });
      },
      failure(resp) {
        this.$notify.error({
          message: resp["msg"],
          duration: 2000
        });
      }
    },
    mounted() {
      var obj = this;

      function temp_func() {
        // obj.getPagination(1)
        obj.getCaseList()
      }

      setTimeout(temp_func, 500)
    }
  }
</script>

<style scoped>

</style>
