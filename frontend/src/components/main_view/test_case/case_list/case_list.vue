<template>

  <div>
    <el-dialog
      title="添加TestCase"
      :visible.sync="DialogVisible"
      width="30%"
      align="center"
    >
      <el-form :model="caseForm"
               :rules="rules"
               label-width="110px"
               class="project"
               close>
        <el-form-item label="用例名称" prop="case_name">
          <el-input v-model="caseForm.case_name"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="DialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleConfirm()">确 定</el-button>
      </div>
    </el-dialog>
    <div style="padding: 10px; text-align: right;">
      <el-select style="width: 343px" v-model="base_url" placeholder="选择API调用">
        <el-option
          v-for="url in url_list"
          :key="url.name"
          :label="url.name + '-> ' + url.value"
          :value="url.value">
        </el-option>
      </el-select>

      <el-button
        icon="el-icon-caret-right"
        type="success"
        round @click="runTest">Run
      </el-button>
    </div>
    <div style="margin-left: 13px">
      <el-button type="primary" plain icon="el-icon-circle-plus" @click="DialogVisible=true">新增用例</el-button>
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
        label="编号"
        width="50">
      </el-table-column>
      <el-table-column

        label="用例"
        width="280">
        <template slot-scope="scope" style="text-align: center">
          <!--<a @click="getCaseItem(scope.row.id)">{{ scope.row.name }}</a>-->
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        width="80">
        <template slot-scope="scope">
          <a><i class="el-icon-edit" style="margin-right: 10px" @click="getCaseItem(scope.row.id)"></i></a>
          <a><i class="el-icon-delete" @click="deleteCaseItem(scope.row.id)"></i></a>
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
        DialogVisible: false,
        caseForm: {
          "case_name": ""
        },
        loading_flag: false,
        multipleSelection: [],
        page: {
          page_now: 1,
          page_previous: null,
          page_next: 2
        },
        arrID: [],
        rules: {
          case_name: [
            {required: true, message: '请输入Case名称', trigger: 'blur'},
            {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
          ]
        },
        base_url: "",
        url_list: []
      }
    },
    methods: {
      handleConfirm() {
        if (this.caseForm.case_name === "") {
          this.$alert('请填写用例名称', '提示', {
            confirmButtonText: '确定',
            callback: action => {

            }
          });
          return
        }

        const project_id = this.$route.params.id;
        var rquest_data = {
          "project_id": project_id,
          "case_name": this.caseForm.case_name
        };
        this.$api.addCase(rquest_data).then(resp => {
            if (resp['success']) {
              this.success(resp);       // 弹出成功提示消息
              this.getCaseList();       // 重新刷新CaseList
            } else {
              this.failure(resp);
            }
          }
        );
        this.caseForm = {
          case_name: ""
        };
        this.DialogVisible = false;

      },
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
          if (resp.success) {
            this.$store.commit("setCaseList", resp["caseList"]);
            this.getCaseItem(this.$store.state.caseList[0].id);
            this.success(resp);       // 弹出成功提示消息
          } else {
            this.failure(resp);
          }
        });
        this.$api.getBaseURLList({"project_id": project_id}).then(resp => {
            this.url_list = resp["BaseURLList"];
          }
        );
      },
      getCaseItem(case_id) {
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
      deleteCaseItem(case_id) {
        // 弹出确认警告提示框
        this.$confirm('此操作将永久删除该测试用例, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          showClose: false
        }).then(() => {
          this.$api.deleteCase({"case_id": case_id}).then(resp => {
            if (resp['success']) {
              this.success(resp);       // 弹出成功提示消息
              this.getCaseList();       // 重新刷新CaseList
            } else {
              this.failure(resp);
            }
          });
        });
        this.$refs.multipleTable.clearSelection(); // 清空checkbox所有选中
      },
      runTest() {
        if (this.base_url === "") {
          this.$notify.warning({
            position: "top-left",
            message: "请选择测试环境！！！",
            duration: 3000
          });
          return
        }

        if (this.arrID.length === 0) {
          this.$notify.warning({
            position: "top-left",
            message: "请选择要执行的测试用例！！！",
            duration: 3000
          });
          return
        }
        this.loading_flag = true;
        this.$emit('e-autotest', this.loading_flag);
        const project_id = this.$route.params.id;
        this.$api.runTestcases({
          "case_list": this.arrID,
          "project_id": project_id,
          "base_url": this.base_url
        }).then(resp => {
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
        this.base_url = ""
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
          duration: 5000
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
