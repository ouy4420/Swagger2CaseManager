<template>
  <div>
    <div>
      <el-dialog
        :title="DialogTitle"
        :visible.sync="DialogVisible"
        width="30%"
        align="center"
        @close="reset_extract_form"
      >
        <el-form :model="extractForm"
                 :rules="rules"
                 ref="extractForm"
                 label-width="110px"
                 class="project">
          <el-form-item label="变量名称" prop="key">
            <el-input v-model="extractForm.key" clearable></el-input>
          </el-form-item>
          <el-form-item label="变量值" prop="value">
            <el-input  v-model="extractForm.value"></el-input>
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
                   @click="DialogVisible = true; DialogTitle='添加Extract'"
                   icon="el-icon-circle-plus">
          添加Extract
        </el-button>
      </div>
    </div>
    <el-table
      highlight-current-row
      :data="this.stepItem.test.extract"
      border
      stripe
      :show-header="this.stepItem.test.extract.length > 0"
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
    name: "Extract",
    props: ["stepItem"],
    data() {
      return {
        DialogTitle: "",
        DialogVisible: false,
        extractForm: {
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
        this.DialogTitle = '编辑Extract'; // 设置dialog title
        this.extractForm.key = row['key'];
        this.extractForm.value = row['value'];
        this.extractForm.id = row['id'];
        this.extractForm.step_id = row['step_id'];
      },
      handleDelete(index, row) {
        // 弹出确认警告提示框
        this.$confirm('此操作将永久删除该Extract, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          // delete 和 post/patch方法的参数不一样，需要加一层data
          this.$api.deleteExtract(row).then(resp => {
            if (resp['success']) {
              this.success(resp);       // 弹出成功提示消息
              this.get_case();          // 重新刷新当前case数据
            } else {
              this.fail_notify(resp)
            }
            this.reset_extract_form()  // 重置表单数据
          })
        })
      },
      reset_extract_form() {
        this.extractForm = {
          key: '',
          value: '',
          id: '',
          config_id: ''
        };
      },
      handleConfirm() {
        this.$refs["extractForm"].validate((valid) => {
          if (valid) {
            // 新建或编辑框中的数据校验通过后，将弹框隐藏掉
            this.DialogVisible = false;
            let obj;
            if (this.extractForm.id === '') {
              this.extractForm.step_id = this.stepItem.step_id;
              obj = this.$api.addExtract(this.extractForm);     // 没有就新建
            } else {
              obj = this.$api.updateExtract(this.extractForm);  // 有就更新
            }
            // 给http response挂载一个处理的钩子
            obj.then(resp => {
              if (resp.success) {
                this.success(resp);       // 弹出成功提示消息
                this.get_case();          // 重新刷新当前case数据
              } else {
                this.fail_notify(resp)
              }
              this.reset_extract_form()  // 重置表单数据
            })
          } else {
            this.DialogVisible = true;
            if (this.extractForm.id !== '') {
              this.DialogTitle = "编辑Extract";  // 已经存在显示编辑框
            } else {
              this.DialogTitle = "新增Extract";  // 不存在显示新建框
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
