<template>
  <div>
    <div>
      <el-dialog
        :title="DialogTitle"
        :visible.sync="DialogVisible"
        width="30%"
        align="center"
        @close="reset_parameter_form"
      >
        <el-form :model="parameterForm"
                 :rules="rules"
                 ref="parameterForm"
                 label-width="110px"
                 class="project">
          <el-form-item label="变量名称" prop="key">
            <el-input v-model="parameterForm.key" clearable>
              <el-select v-model="parameterForm.value_type" slot="prepend" placeholder="变量类型" style="width: 110px">
                <el-option label="参数列表" value="json_list"></el-option>
                <el-option label="自定义函数" value="defined_func"></el-option>
              </el-select>
            </el-input>
          </el-form-item>
          <el-form-item label="变量值" prop="value">
            <el-input placeholder="请输入对应变量类型值" v-model="parameterForm.value"></el-input>
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
                   @click="handleAdd"
                   icon="el-icon-circle-plus">
          添加Parameter
        </el-button>
      </div>
    </div>
    <el-table
      highlight-current-row
      :data="this.$store.state.currentCase['config'].config.parameters"
      border
      stripe
      :show-header="this.$store.state.currentCase['config'].config.parameters.length > 0"
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
    name: "Parameters",
    data() {
      return {
        DialogTitle: "",
        DialogVisible: false,
        parameterForm: {
          key: '',
          value: '',
          value_type: '',
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
      handleAdd() {
        this.DialogVisible = true;           // 弹出添加框
        this.DialogTitle = '添加Parameter'     // 设置dialog title
      },
      handleEdit(index, row) {
        this.DialogVisible = true;           // 弹出编辑框
        this.DialogTitle = '编辑Parameter';  // 设置dialog title
        // 显示要编辑的数据 ---------------------------------------
        this.parameterForm.key = row['key'];
        this.parameterForm.value_type = row["value_type"];
        this.parameterForm.id = row['id'];
        this.parameterForm.config_id = row['config_id'];

        if (row['value_type'] === "json_list"){
          this.parameterForm.value = JSON.stringify(row["value"], null, 0);  // 格式化显示, list不需要空格
        }else{
          this.parameterForm.value = row['value']
        }
      },
      handleDelete(index, row) {
        // 弹出确认警告提示框
        this.$confirm('此操作将永久删除该Parameter, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          // delete 和 post/patch方法的参数不一样，需要加一层data
          this.$api.deleteParameter(row).then(resp => {
            if (resp['success']) {
              this.success(resp);       // 弹出成功提示消息
              this.get_case();          // 重新刷新当前case数据
            } else {
              this.fail_notify(resp)
            }
            this.reset_parameter_form()  // 重置表单数据
          })
        })
      },
      reset_parameter_form() {
        this.parameterForm = {
          key: '',
          value: '',
          value_type: '',
          id: '',
          config_id: ''
        };
      },
      check_value_type(){
        // 参数校验之选择value_type --------------------------------------
            if (this.parameterForm["value_type"] === "") {
              this.$notify.error({
                message: "请选择变量值的参数类型！",
                duration: 5000
              });
              return false
            }
            // 参数校验之校验value_type对应的value --------------------------------------
            if (this.parameterForm.value_type === "json_list") {
              try {
                JSON.stringify(JSON.parse(this.parameterForm.value), null, 0);
              } catch (err) {
                this.reset_parameter_form();
                this.$notify.error({
                  message: "非Json_list格式数据，请校验后重新编辑！",
                  duration: 5000
                });
                return false
              }
            }
            return true
      },
      handleConfirm() {
        this.$refs["parameterForm"].validate((valid) => {
          if (valid) {
            var flag = this.check_value_type()
            if (flag === false){
              return
            }
            this.DialogVisible = false;  // 新建或编辑框中的数据校验通过后，将弹框隐藏掉
            let obj;
            if (this.parameterForm.id === '') {
              // 没有就新建
              this.parameterForm.config_id = this.$store.state.currentCase['config'].config_id;
              obj = this.$api.addParameter(this.parameterForm);
            } else {
              // 有就更新
              obj = this.$api.updateParameter(this.parameterForm);
            }
            // 给http response挂载一个处理的钩子
            obj.then(resp => {
              if (resp.success) {
                this.success(resp);       // 弹出成功提示消息
                this.get_case();          // 重新刷新当前case数据
              } else {
                this.fail_notify(resp)
              }
              this.reset_parameter_form()  // 重置表单数据
            })
          } else {
            this.DialogVisible = true;
            if (this.parameterForm.id !== '') {
              this.DialogTitle = "编辑Parameter";  // 已经存在显示编辑框
            } else {
              this.DialogTitle = "新增Parameter";  // 不存在显示新建框
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
        // console.log("in get_case2", this.parameterForm);
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
