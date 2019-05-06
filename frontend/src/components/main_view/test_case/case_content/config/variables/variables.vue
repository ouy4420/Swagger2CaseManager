<template>
  <div>
    <div>
      <el-dialog
        :title="DialogTitle"
        :visible.sync="DialogVisible"
        width="30%"
        align="center"
        @close="reset_variable_form"
      >
        <el-form :model="variableForm"
                 :rules="rules"
                 ref="variableForm"
                 label-width="110px"
                 class="project">
          <el-form-item label="变量名称" prop="key">
            <el-input v-model="variableForm.key" clearable></el-input>
          </el-form-item>
          <el-form-item label="变量值" prop="value">
            <el-input v-model="variableForm.value" clearable></el-input>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
                        <el-button @click="DialogVisible = false">取消</el-button>
                        <el-button type="primary" @click="handleConfirm()">确 定</el-button>
                      </span>
      </el-dialog>
      <div style="">
        <el-button type="primary"
                   size="small"
                   @click="DialogVisible = true; DialogTitle='添加Variable'"
                   icon="el-icon-circle-plus">
          添加Variable
        </el-button>
      </div>
    </div>
    <el-table
      highlight-current-row
      :data="this.$store.state.currentCase['config'].config.variables"
      border
      stripe
      :show-header="this.$store.state.currentCase['config'].config.variables.length > 0"
      style="width: 100%;"
    >
      <el-table-column
        label="key"
        width="200"
        align="center"
      >
        <template slot-scope="scope">
                      <span
                        style="font-size: 18px; font-weight: bold; cursor: pointer;"
                        @click="handleCellClick(scope.row)"
                      >{{ scope.row.key }}
                            </span>
        </template>
      </el-table-column>

      <el-table-column
        label="value"
        width="800"
        align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.value }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        align="center"
      >
        <template slot-scope="scope">
          <el-button
            size="medium"
            type="primary"
            @click="handleEdit(scope.$index, scope.row)">编辑
          </el-button>

          <el-button
            size="medium"
            type="danger"
            @click="handleDelete(scope.$index, scope.row)">删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>


  export default {
    name: "Variables",
    data() {
      return {
        DialogTitle: "",
        DialogVisible: false,
        variableForm: {
          key: '',
          value: '',
          id: '',
          config_id: ''
        },
        rules: {
          key: [
            {required: true, message: '请输入变量名称', trigger: 'blur'},
            {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
          ],
          value: [
            {required: true, message: '请输入变量值', trigger: 'blur'},
            {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
          ]
        }
      }
    },
    methods: {
      handleEdit(index, row) {
        this.DialogVisible = true; // 弹出编辑框
        this.DialogTitle = '编辑Variable'; // 设置dialog title
        this.variableForm.key = row['key'];
        if (typeof row['value'] == "object") {
          this.variableForm.value = JSON.stringify(row['value']);
        } else {
          this.variableForm.value = row['value'];
        }
        this.variableForm.id = row['id'];
        this.variableForm.config_id = row['config_id'];
      },
      handleDelete(index, row) {
        // 弹出确认警告提示框
        this.$confirm('此操作将永久删除该项目, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          // delete 和 post/patch方法的参数不一样，需要加一层data
          this.$api.deleteVariable(row).then(resp => {
            if (resp['success']) {
              this.success(resp);       // 弹出成功提示消息
              this.get_case();          // 重新刷新当前case数据
            } else {
              this.failure(resp);
            }
            this.reset_variable_form()  // 重置表单数据
          })
        })
      },
      reset_variable_form() {
        this.variableForm = {
          key: '',
          value: '',
          id: '',
          config_id: ''
        };
      },
      handleConfirm() {
        console.log(1111, this.$refs["variableForm"])
        this.$refs["variableForm"].validate((valid) => {
          if (valid) {
            // 新建或编辑框中的数据校验通过后，将弹框隐藏掉
            this.DialogVisible = false;
            let obj;
            if (this.variableForm.id === '') {
              this.variableForm.config_id = this.$store.state.currentCase['config'].config_id;
              obj = this.$api.addVariable(this.variableForm);     // 没有就新建
            } else {
              obj = this.$api.updateVariable(this.variableForm);  // 有就更新
            }
            // 给http response挂载一个处理的钩子
            obj.then(resp => {
              if (resp.success) {
                this.success(resp);       // 弹出成功提示消息
                this.get_case();          // 重新刷新当前case数据
              } else {
                this.failure(resp);
              }
              this.clear_variable_form()  // 重置表单数据
            })
          } else {
            this.DialogVisible = true;
            if (this.variableForm.id !== '') {
              this.DialogTitle = "编辑Variable";  // 已经存在显示编辑框
            } else {
              this.dialogVisible = "新增Variable";  // 不存在显示新建框
            }
            return false;
          }
        });

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
        // console.log("in get_case2", this.variableForm);
        // console.log("in get_case is.$store.state.currentCase", this.$store.state.currentCase);
        var currentCaseID = this.$store.state.currentCase['config'].case_id;
        this.$api.getCaseDetail(currentCaseID).then(resp => {
          console.log("in getCaseDetail", resp);
          this.$store.commit('setCurrentCase', resp);
        });
      }
    },
    mounted() {

    }
  }
</script>

<style scoped>

</style>
