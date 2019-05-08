<template>

  <div>
    <div style="padding: 10px; text-align: right; margin-bottom: 20px">
      <el-button type="success" round @click="runTest">执行测试</el-button>
    </div>
    <el-table
      @row-click="handleCurrentChange"
      @selection-change="selsChange"
      ref="multipleTable"
      :data="caseList"
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
        label=""
        width="240">
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
        caseList: [],
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
      handleSelectionChange(val) {
        console.log("this.multipleSelection: ", this.multipleSelection)
        console.log("this.his.$refs.multipleTable: ", this.$refs.multipleTable)
        this.multipleSelection = val;
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
        console.log("project_id",project_id)
        console.log("this.$route.params.id",this.$route.params.id)
        this.$api.getCaseList({"id": project_id}).then(resp => {
          this.caseList = resp["caseList"];
          this.setCaseItem(this.caseList[0].id);
        })
      },
      setCaseItem(case_id) {
        this.$api.getCaseDetail(case_id).then(resp => {
          this.$store.commit('setCurrentCase', resp);
          window.scrollTo(0, 0); // 滚动条弹到顶端
          this.$refs.multipleTable.clearSelection(); // 清空checkbox所有选中

        });
      },
      runTest(){
        const project_id = this.$route.params.id;
        this.$api.runTestcases({"case_list": this.arrID, "project_id": project_id}).then(resp => {

          if (resp['success']) {
            var render_content = resp.render_content;
            this.success(resp);       // 弹出成功提示消息
            var newWin = window.open("", "_blank");
            newWin.document.write(render_content)
          } else {
            this.failure(resp);
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
          duration: 3000
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
