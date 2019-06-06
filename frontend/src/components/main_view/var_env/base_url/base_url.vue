<template>
  <el-container>
    <el-dialog
      :title="DialogTitle"
      :visible.sync="DialogVisible"
      width="30%"
      align="center"
      @close="reset_var_form"
    >
      <el-form :model="varForm"
               :rules="rules"
               ref="varForm"
               label-width="110px"
               class="project"
               close>
        <el-form-item label="环境名称" prop="name">
          <el-input v-model="varForm.name"></el-input>
        </el-form-item>
        <el-form-item label="BaseURL" prop="value">
          <el-input v-model="varForm.value"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="DialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleConfirm()">确 定</el-button>
      </div>
    </el-dialog>
    <el-header>
      <div style="padding: 10px; text-align: left; margin-top: 10px">
        <el-button type="primary" plain icon="el-icon-circle-plus" @click="DialogVisible=true">新增环境</el-button>
      </div>
    </el-header>

    <el-container>
      <el-main style="padding: 0; margin-top: 20px;margin-left: 10px; margin-right: 10px">
        <el-table
          highlight-current-row
          :data="BaseURLList"
          border
          stripe
          :show-header="BaseURLList.length > 0"
          style="width: 60%;"
        >
          <el-table-column
            label="编号"
            width="200"
            align="center"
          >
            <template slot-scope="scope">
                      <span
                        style="font-size: 18px; font-weight: bold; cursor: pointer;"
                        @click="handleCellClick(scope.row)"
                      >{{ scope.row.index }}
                            </span>
            </template>
          </el-table-column>

          <el-table-column
            label="环境名称"
            width="187"
            align="center"
          >
            <template slot-scope="scope">
                      <span
                        style="font-size: 18px; font-weight: bold; cursor: pointer;"
                        @click="handleCellClick(scope.row)"
                      >{{ scope.row.name }}
                            </span>
            </template>
          </el-table-column>

          <el-table-column
            label="BaseURL"
            width="362"
            align="center"
          >
            <template slot-scope="scope">
              <span>{{ scope.row.value }}</span>
            </template>
          </el-table-column>
          <el-table-column
            label="操作"
            align="center"
            width="300"
          >
            <template slot-scope="scope">
              <el-button
                size="medium"
                type="info"
                icon="el-icon-edit"
                @click="handleEdit(scope.$index, scope.row)">编辑
              </el-button>
              <el-button
                size="medium"
                type="danger"
                icon="el-icon-delete"
                @click="handleDelete(scope.$index, scope.row)">删除
              </el-button>
            </template>
          </el-table-column>

        </el-table>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>

  export default {
    components: {},
    props: ["BaseURLList"],
    data() {
      return {
        varForm: {
          name: "",
          value: "",
          id: ""
        },
        DialogVisible: false,
        DialogTitle: "",
        rules: {
          name: [
            {required: true, message: '请输入变量名', trigger: 'blur'},
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
        this.DialogTitle = '添加环境配置'     // 设置dialog title
      },
      handleEdit(index, row) {
        this.DialogVisible = true;           // 弹出编辑框
        this.DialogTitle = '编辑环境配置';  // 设置dialog title

        // 显示要编辑的数据 ---------------------------------------
        this.varForm.name = row['name'];
        this.varForm.value = row['value'];
        this.varForm.id = row['id'];
      },
      handleDelete(index, row) {
        // 弹出确认警告提示框
        this.$confirm('此操作将永久删除该环境配置, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          // delete 和 post/patch方法的参数不一样，需要加一层data
          this.$api.deleteBaseURL({"id": row.id}).then(resp => {
            if (resp['success']) {
              this.success(resp);       // 弹出成功提示消息
              this.$emit('refresh', true);
            } else {
              this.fail_notify(resp)
            }
            this.reset_var_form()  // 重置表单数据
          })
        })
      },
      reset_var_form() {
        this.varForm = {
          name: "",
          value: "",
          id: ""
        }
      },
      handleConfirm() {
        this.$refs["varForm"].validate((valid) => {
          if (valid) {
            this.DialogVisible = false;  // 新建或编辑框中的数据校验通过后，将弹框隐藏掉
            let obj;
            if (this.varForm.id === '') {
              // 没有就新建
              this.varForm.project_id = this.$route.params.id;
              obj = this.$api.addBaseURL({"obj": this.varForm});
            } else {
              // 有就更新
              obj = this.$api.updateBaseURL({"obj": this.varForm});
            }
            // 给http response挂载一个处理的钩子
            obj.then(resp => {
              if (resp.success) {
                this.success(resp);       // 弹出成功提示消息
                this.$emit('refresh', true);
              } else {
                this.fail_notify(resp)
              }
              this.reset_var_form()  // 重置表单数据
            })
          } else {
            this.DialogVisible = true;
            if (this.varForm.id !== '') {
              this.DialogTitle = "编辑环境变量";  // 已经存在显示编辑框
            } else {
              this.DialogTitle = "新增环境变量";  // 不存在显示新建框
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
    },
    mounted() {

    }
  }
</script>

<style scoped>

</style>
