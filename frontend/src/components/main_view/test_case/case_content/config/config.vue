<template>

<div>
    <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
    <el-tab-pane label="Name" name="name">
      {{this.$store.state.currentCase['config'].config.name}}
    </el-tab-pane>
    <el-tab-pane label="Parameters" name="parameters">
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
            width="200"
            align="center"
          >
            <template slot-scope="scope">
              <span>{{ scope.row.value }}</span>
            </template>
          </el-table-column>
        </el-table>
    </el-tab-pane>
    <el-tab-pane label="Request" name="request">
      角色管理
    </el-tab-pane>
    <el-tab-pane label="Variables" name="variables">
       <div>
        <div style="">
          <el-button type="primary"
                     size="small"
                     @click="dialogVisible = true"
                      icon="el-icon-circle-plus">
            添加Variable
          </el-button>


          <el-dialog
            title="添加Variable"
            :visible.sync="dialogVisible"
            width="30%"
            align="center"
          >
            <el-form :model="variableForm"
                     :rules="rules"
                     ref="variableForm"
                     label-width="110px"
                     class="project">
              <el-form-item label="变量名称" prop="name">
                <el-input v-model="variableForm.key" clearable></el-input>
              </el-form-item>
              <el-form-item label="变量值" prop="url">
                <el-input v-model="variableForm.value" clearable></el-input>
              </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                        <el-button @click="dialogVisible = false">取消</el-button>
                        <el-button type="primary" @click="handleConfirm('variableForm')">确 定</el-button>
                      </span>
          </el-dialog>
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

              <el-dialog
                title="编辑Variable"
                :visible.sync="editVisible"
                width="30%"
              >
                <el-form :model="variableForm"
                         :rules="rules"
                         ref="variableForm"
                         label-width="100px"
                         class="project">
                  <el-form-item label="变量名称" prop="name">
                    <el-input v-model="variableForm.key" clearable></el-input>
                  </el-form-item>
                  <el-form-item label="变量值" prop="desc">
                    <el-input v-model="variableForm.value" clearable></el-input>
                  </el-form-item>
                </el-form>
                <span slot="footer" class="dialog-footer">
                        <el-button @click="editVisible = false">取 消</el-button>
                        <el-button type="primary" @click="handleConfirm('variableForm')">确 定</el-button>
                      </span>
              </el-dialog>


              <el-button
                size="medium"
                type="danger"
                @click="handleDelete(scope.$index, scope.row)">删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
    </el-tab-pane>
  </el-tabs>
</div>

</template>

<script>

  export default {
    name: "Config",
    data() {
      return {
        activeName: 'name',
        editVisible: false,
        dialogVisible: false,
        current_case_id: null,
        variableForm: {
          key: '',
          value: '',
          id: '',
          config_id: '',
          case_id: ''
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
      handleClick(tab, event) {
          console.log(1,tab);
          console.log(2, event);
        },
      handleEdit(index, row) {
        console.log("row data: ",  row);
        this.editVisible = true;  // 弹出编辑框
        this.variableForm.key = row['key'];
        this.variableForm.value = JSON.stringify(row['value']);
        this.variableForm.id = row['id'];
        this.variableForm.config_id = row['config_id'];
        this.variableForm.case_id = row['case_id'];
      },
      handleDelete(index, row) {
        this.variableForm.key = row['key'];
        this.variableForm.value = JSON.stringify(row['value']);
        this.variableForm.id = row['id'];
        this.variableForm.config_id = row['config_id'];
        this.variableForm.case_id = row['case_id'];
        // 弹出确认警告提示框
        this.$confirm('此操作将永久删除该项目, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          // delete 和 post/patch方法的参数不一样，需要加一层data
          this.$api.deleteVariable(row).then(resp => {
            if (resp['success']) {
              this.success(resp);
              this.get_case();
            } else {
              this.failure(resp);
            }
          })
        })
      },
      handleConfirm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            // 新建或编辑框中的数据校验通过后，将弹框隐藏掉
            this.dialogVisible = false;
            this.editVisible = false;
            let obj;
            console.log("1", this.variableForm);
            if (this.variableForm.id === '') {
              this.variableForm.config_id = this.$store.state.currentCase['config'].config_id;
              console.log("2", this.variableForm);
              obj = this.$api.addVariable(this.variableForm);     // 没有就新建
            } else {
              obj = this.$api.updateVariable(this.variableForm);  // 有就更新
            }
            // 给http response挂载一个处理的钩子
            console.log("1-------------------------------")
            obj.then(resp => {
              console.log("1-------------------------------")
              if (resp.success) {
                this.success(resp);
                this.get_case();
              } else {
                this.failure(resp);
              }
              console.log("2-------------------------------")
              this.variableForm.key = '';
              this.variableForm.value = '';
              this.variableForm.id = '';
              this.variableForm.config_id = '';
            })
          } else {
            if (this.variableForm.id !== '') {
              this.editVisible = true;  // 已经存在显示编辑框
            } else {
              this.dialogVisible = true;  // 不存在显示新建框
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
        console.log("in get_case2", this.variableForm)
        this.$api.getCaseDetail(this.variableForm.case_id).then(resp => {
          console.log("in getCaseDetail", resp)
          this.$store.commit('setCurrentCase', resp);
        });
      }
    },
    mounted() {
      var obj = this;
      function temp_func(){
          var state = obj.$store.state;
      var user = state.user;
      var token = state.token;
      var currentCase = state.currentCase;
      obj.config = currentCase["config"];
      console.log(666, "user", user);
      console.log(666, "token", token);
      console.log(666, "currentCase", currentCase)
      }
      // setTimeout(temp_func,1000);
      // // this.config = this.$store.state.currentCase;


    }
  }
</script>

<style scoped>

</style>
