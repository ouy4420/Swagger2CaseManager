<template>
  <div>
    <div>
      <el-dialog
        :title="DialogTitle"
        :visible.sync="DialogVisible"
        width="30%"
        align="center"
        @close="reset_validate_form"
      >
        <el-form :model="validateForm"
                 :rules="rules"
                 ref="validateForm"
                 label-width="110px"
                 class="project">
          <el-form-item label="断言类型" prop="comparator">
            <el-input v-model="validateForm.comparator" clearable></el-input>
          </el-form-item>
          <el-form-item label="校验值" prop="check">
            <el-input v-model="validateForm.check" clearable></el-input>
          </el-form-item>
          <el-form-item label="期望值" prop="expected">
            <el-input placeholder="输入期望值前，请选择好参数类型" v-model="validateForm.expected" class="input-with-select">
              <el-select v-model="validateForm.expected_type" slot="prepend" placeholder="参数类型" style="width: 110px">
                <el-option label="int" value="int"></el-option>
                <el-option label="str" value="str"></el-option>
              </el-select>
            </el-input>
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
                   @click="DialogVisible = true; DialogTitle='添加Validate'"
                   icon="el-icon-circle-plus">
          添加Validate
        </el-button>
      </div>
    </div>
    <el-table
      highlight-current-row
      :data="stepItem.test.validate"
      border
      stripe
      :show-header="stepItem.test.validate.length > 0"
      style="width: 100%;"
    >
      <el-table-column
        label="断言类型"
        width="200"
        align="center"
      >
        <template slot-scope="scope">
                      <span
                        style="font-size: 18px; font-weight: bold; cursor: pointer;"
                      >{{ scope.row.comparator }}
                            </span>
        </template>
      </el-table-column>

      <el-table-column
        label="校验值"
        width="300"
        align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.check }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="期望值"
        width="300"
        align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.expected }}</span>
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
    name: "Validate",
    props: ["stepItem"],
    data() {
      return {
        DialogTitle: "",
        DialogVisible: false,
        validateForm: {
          comparator: '',
          check: '',
          expected: '',
          expected_type: '',
          id: '',
          step_id: ''
        },
        rules: {
          comparator: [
            {required: true, message: '请输入校验类型', trigger: 'blur'},
            {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
          ],
          check: [
            {required: true, message: '请输入校验值', trigger: 'blur'},
            {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
          ],
          expected: [
            {required: true, message: '请输入期望值', trigger: 'blur'},
            {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
          ]
        }
      }
    },
    methods: {
      handleEdit(index, row) {
        this.DialogVisible = true; // 弹出编辑框
        this.DialogTitle = '编辑Validate'; // 设置dialog title
        this.validateForm.comparator = row['comparator'];
        this.validateForm.check = row['check'];
        this.validateForm.expected = row['expected'];
        this.validateForm.id = row['id'];
        this.validateForm.step_id = row['step_id'];
      },
      handleDelete(index, row) {
        // 弹出确认警告提示框
        this.$confirm('此操作将永久删除该Validate, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          // delete 和 post/patch方法的参数不一样，需要加一层data
          this.$api.deleteValidate(row).then(resp => {
            if (resp['success']) {
              this.success(resp);       // 弹出成功提示消息
              this.get_case();          // 重新刷新当前case数据
            } else {
              this.fail_notify(resp)
            }
            this.reset_validate_form()  // 重置表单数据
          })
        })
      },
      reset_validate_form() {
        this.validateForm = {
          comparator: '',
          check: '',
          expected: '',
          expected_type: '',
          id: '',
          step_id: ''
        };
      },
      check_value_type() {
        // 参数校验之选择value_type --------------------------------------
        if (this.validateForm["expected_type"] === "") {
          this.$alert('请选择期望值的参数类型！', '注意', {
            confirmButtonText: '确定',
            callback: action => {

            }
          });

          return false
        }
        // 参数校验之校验value_type对应的value --------------------------------------
        if (this.validateForm.expected_type === "int") {
          var value = Number(this.validateForm.expected);
          if (window.isNaN(value)) {
            this.reset_validate_form();
            this.$alert('非Int类型格式数据，请校验后重新编辑！', '注意', {
              confirmButtonText: '确定',
              callback: action => {

              }
            });
            return false
          }
        }
        return true
      },
      handleConfirm() {
        this.$refs["validateForm"].validate((valid) => {
          if (valid) {
            var flag = this.check_value_type();
            if (flag === false) {
              return
            }

            // 新建或编辑框中的数据校验通过后，将弹框隐藏掉
            this.DialogVisible = false;
            let obj;
            if (this.validateForm.id === '') {
              this.validateForm.step_id = this.stepItem.step_id;
              obj = this.$api.addValidate({"validateForm": this.validateForm});     // 没有就新建
            } else {
              obj = this.$api.updateValidate({"validateForm": this.validateForm});  // 有就更新
            }
            // 给http response挂载一个处理的钩子
            obj.then(resp => {
              if (resp.success) {
                this.success(resp);       // 弹出成功提示消息
                this.get_case();          // 重新刷新当前case数据
              } else {
                this.fail_notify(resp)
              }
              this.reset_validate_form()  // 重置表单数据
            })
          } else {
            this.DialogVisible = true;
            if (this.validateForm.id !== '') {
              this.DialogTitle = "编辑Validate";  // 已经存在显示编辑框
            } else {
              this.DialogTitle = "新增Validate";  // 不存在显示新建框
            }
            return false;
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

</style>
