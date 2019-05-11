<template>
  <div>
    <div>
      <el-dialog
        :title="DialogTitle"
        :visible.sync="DialogVisible"
        width="30%"
        align="center"
        @close="reset_variable_form">

        <el-form :model="variableForm"
                 :rules="rules"
                 ref="variableForm"
                 label-width="110px"
                 class="project"
                 close>
          <el-form-item label="变量名称" prop="key">
            <el-input v-model="variableForm.key" clearable>
              <el-select v-model="variableForm.value_type" slot="prepend" placeholder="参数类型" style="width: 110px">
                <el-option label="json" value="json"></el-option>
                <el-option label="int" value="int"></el-option>
                <el-option label="str" value="str"></el-option>
              </el-select>
            </el-input>
          </el-form-item>
          <el-form-item label="变量值" prop="value">
            <el-input type="textarea" v-model="variableForm.value"></el-input>
          </el-form-item>

        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="DialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleConfirm()">确 定</el-button>
          <!--<el-button type="primary" @click="innerVisible = true">打开内层 Dialog</el-button>-->
        </div>
      </el-dialog>
      <div style="">
        <el-button type="primary"
                   size="small"
                   @click="handleAdd"
                   icon="el-icon-circle-plus">
          添加Variable
        </el-button>
      </div>
    </div>
    <el-table
      highlight-current-row
      :data="stepItem.test.variables"
      border
      stripe
      :show-header="stepItem.test.variables.length > 0"
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
    components: {},
    props: ["stepItem"],
    data() {
      return {
        innerVisible: false,
        DialogTitle: "",
        DialogVisible: false,
        variableForm: {
          key: '',
          value: '',
          value_type: '',
          id: '',
          step_id: ''
        },
        rules: {
          key: [
            {required: true, message: '请输入变量名称', trigger: 'blur'},
            {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
          ],
          value: [
            {required: true, message: '请输入变量值', trigger: 'blur'},
            {min: 1, max: 99999999, message: '最多不超过50个字符', trigger: 'blur'}
          ]
        }
      }
    },
    methods: {
      handleAdd(){
        this.DialogVisible = true; // 弹出编辑框
        this.DialogTitle = '新增Variable'; // 设置dialog title
      },
      handleEdit(index, row) {
        this.DialogVisible = true; // 弹出编辑框
        this.DialogTitle = '编辑Variable'; // 设置dialog title
        this.variableForm.key = row['key'];
        this.variableForm.value_type = row['value_type'];
        this.variableForm.id = row['id'];
        this.variableForm.step_id = row['step_id'];

        if (row['value_type'] === "json"){
          this.variableForm.value = JSON.stringify(row["value"], null, 2);  // 格式化显示
        }else{
          this.variableForm.value = row['value']
        }
      },
      handleDelete(index, row) {
        // 弹出确认警告提示框
        this.$confirm('此操作将永久删除该项目, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          // delete 和 post/patch方法的参数不一样，需要加一层data
          this.$api.deleteVariableLocal(row).then(resp => {
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
          value_type: '',
          id: '',
          step_id: ''
        };
      },
      check_value_type() {
        if (this.variableForm["value_type"] === "") {
          this.$notify.error({
            message: "请选择变量值的参数类型！",
            duration: 5000
          });
          return false
        }
        var value_type = this.variableForm["value_type"];
        if (value_type === "json") {
          try {
            JSON.parse(this.variableForm.value);
          } catch (err) {
            this.reset_variable_form();
            this.$notify.error({
              message: "非Json格式数据，请校验后重新编辑！",
              duration: 5000
            });
            return false
          }
        }
        else if (value_type === "int") {
          var value = Number(this.variableForm.value);
          if (window.isNaN(value)) {
            this.reset_variable_form();
            this.$notify.error({
              message: "非Int类型格式数据，请校验后重新编辑！",
              duration: 5000
            });
            return false
          }
        }
        return true
      },
      handleConfirm() {
        this.$refs["variableForm"].validate((valid) => {
          if (valid) {
            // 参数校验之选择value_type --------------------------------------
            var flag = this.check_value_type();
            if (flag === false){
              return
            }
            // 新建或编辑框中的数据校验通过后，将弹框隐藏掉
            this.DialogVisible = false;
            let obj;
            if (this.variableForm.id === '') {
              this.variableForm.step_id = this.stepItem.step_id;
              obj = this.$api.addVariableLocal(this.variableForm);     // 没有就新建
            } else {
              obj = this.$api.updateVariableLocal(this.variableForm);  // 有就更新
            }
            // 给http response挂载一个处理的钩子
            obj.then(resp => {
              if (resp.success) {
                this.success(resp);       // 弹出成功提示消息
                this.get_case();          // 重新刷新当前case数据
              } else {
                this.failure(resp);
              }
              this.reset_variable_form()  // 重置表单数据
            })
          } else {
            this.DialogVisible = true;
            if (this.variableForm.id !== '') {
              this.DialogTitle = "编辑Variable";  // 已经存在显示编辑框
            } else {
              this.DialogTitle = "新增Variable";  // 不存在显示新建框
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


<style>
  #xxx {
    height: 200px;
  }
</style>




