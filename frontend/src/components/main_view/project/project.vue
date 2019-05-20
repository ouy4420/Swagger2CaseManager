<template>
  <el-container>
    <el-header
      style="background: #b4f196; padding: 0; height: 70px; margin-left: 0"
      v-loading="loading_flag"
      element-loading-text="拼命加载中，请稍后..."
    >
      <div>
        <div style="padding-top: 20px; margin-left: 10px; padding-bottom: 20px;">
          <el-button
            icon="el-icon-circle-plus"
            size="small"
            @click="dialogVisible = true; urlVisible = false; fileVisible=false">
            添加项目
          </el-button>

          <el-dropdown style="margin-left: 10px">
            <span class="el-dropdown-link">
              <i class="el-icon-s-promotion"></i>
              Swagger导入<i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>
                <span
                  @click="dialogVisible = true; urlVisible = true; fileVisible=false">
                  URL方式
                </span>
              </el-dropdown-item>
              <el-dropdown-item>
                <span
                  @click="dialogVisible = true; urlVisible = false; fileVisible=true">
                  文件方式
                </span>
              </el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
          <el-dialog
            title="添加项目"
            :visible.sync="dialogVisible"
            width="30%"
            align="center"
            @close="close_dialog"
          >
            <el-form :model="projectForm"
                     :rules="rules"
                     ref="projectForm"
                     label-width="110px"
                     class="project">
              <el-form-item label="ProjectName" prop="name">
                <el-input v-model="projectForm.name" clearable></el-input>
              </el-form-item>
              <el-form-item v-if="urlVisible" label="SwaggerUrl" prop="url">
                <el-input v-model="projectForm.url" clearable></el-input>
              </el-form-item>
              <el-form-item label="Description" prop="desc">
                <el-input v-model="projectForm.desc" clearable></el-input>
              </el-form-item>
              <el-form-item v-if="fileVisible" label="文件上传" prop="file">
                <my-upload></my-upload>
              </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                        <el-button @click="dialogVisible = false">取消</el-button>
                        <el-button type="primary" @click="handleConfirm('projectForm')">确 定</el-button>
                      </span>
          </el-dialog>
        </div>
      </div>
    </el-header>

    <el-container>
      <el-main style="padding: 0;">
        <div style="padding: 10px; text-align: right; margin-right: 60px">
          <el-button style="margin-left: 50px"
                     type="info"
                     round
                     size="small"
                     icon="el-icon-menu"
                     @click="getPagination(1)"
          >
            首页
          </el-button>
          <el-button
            type="info"
            round
            size="small"
            icon="el-icon-d-arrow-left"
            :disabled="page.page_previous === null "
            @click="getPagination(page.page_previous)"
          >
            上一页
          </el-button>

          <el-button
            type="info"
            round
            size="small"
            :disabled="page.page_next === null"
            @click="getPagination(page.page_next)"
          >
            下一页
            <i class="el-icon-d-arrow-right"></i>
          </el-button>
        </div>
        <el-table
          :data="projectData"
          style="width: 100%">
          <el-table-column type="expand">
            <template slot-scope="props">
              <el-form label-position="left" inline class="demo-table-expand">
                <el-form-item label="接口总数: ">
                  <span><strong>{{ props.row.len_api }}</strong> 个API</span>
                </el-form-item>
                <el-form-item label="用例总数: ">
                  <span><strong>{{ props.row.len_case }}</strong> 个用例</span>
                </el-form-item>
                <el-form-item label="环境总数 :">
                  <span><strong>{{ props.row.len_baseurl }}</strong> 个环境</span>
                </el-form-item>
                <el-form-item label="报告总数">
                  <span><strong>{{ props.row.len_report }}</strong> 个报告</span>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>
          <el-table-column
            label="编号"
            prop="index">
          </el-table-column>
          <el-table-column
            label="项目名称"
            prop="name">
          </el-table-column>
          <el-table-column
            label="负责人"
            prop="responsible">
          </el-table-column>
          <el-table-column
            label="创建方式"
            prop="mode">
          </el-table-column>
          <el-table-column
            label="项目描述"
            prop="desc">
          </el-table-column>
          <el-table-column
            label="操作"
            align="center"
          >
            <template slot-scope="scope">
              <el-button
                size="medium"
                @click="handleCellClick(scope.row)">管理
              </el-button>

              <el-button
                size="medium"
                type="primary"
                @click="handleEdit(scope.$index, scope.row)">编辑
              </el-button>

              <el-dialog
                title="编辑项目"
                :visible.sync="editVisible"
                width="30%"
                @close="close_dialog"
              >
                <el-form :model="projectForm"
                         :rules="rules"
                         ref="projectForm"
                         label-width="100px"
                         class="project">
                  <el-form-item label="项目名称" prop="name">
                    <el-input v-model="projectForm.name" clearable></el-input>
                  </el-form-item>
                  <el-form-item label="项目描述" prop="desc">
                    <el-input v-model="projectForm.desc" clearable></el-input>
                  </el-form-item>
                </el-form>
                <span slot="footer" class="dialog-footer">
        <el-button @click="editVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleConfirm('projectForm')">确 定</el-button>
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

      </el-main>


    </el-container>

  </el-container>
</template>

<script>
  import upload from "./upload/upload"

  export default {
    components: {
      "my-upload": upload
    },
    data() {
      return {
        loading_flag: false,
        fileVisible: false,
        urlVisible: false,
        dialogVisible: false,
        editVisible: false,
        projectData: {
          results: []
        },
        projectForm: {
          name: '',
          url: '',
          file: this.$store.state.fileConent,
          desc: '',
          responsible: this.$store.state.user,
          id: ''
        },
        rules: {
          name: [
            {required: true, message: '请输入项目名称', trigger: 'blur'},
            {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
          ],
          url: [
            {required: true, message: '请输入swagger url', trigger: 'blur'},
            {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
          ],
          desc: [
            {required: true, message: '简要描述下该项目', trigger: 'blur'},
            {min: 1, max: 100, message: '最多不超过100个字符', trigger: 'blur'}
          ]
        },
        page: {
          page_now: 1,
          page_previous: null,
          page_next: 2
        }
      }
    },
    methods: {
      handleCellClick(row) {
        this.$store.commit('setRouterName', 'AutoTest');
        this.setLocalValue("routerName", 'AutoTest');
        this.$router.push({name: 'AutoTest', params: {id: row['id']}});
      },
      handleEdit(index, row) {
        this.editVisible = true;  // 弹出编辑框
        this.projectForm.name = row['name'];
        this.projectForm.desc = row['desc'];
        this.projectForm.id = row['id'];
      },
      close_dialog() {
        this.projectForm = {
          name: '',
          url: '',
          file: this.$store.state.fileConent,
          desc: '',
          responsible: this.$store.state.user,
          id: ''
        };
      },
      handleDelete(index, row) {
        console.log("index: ", index);
        console.log("row: ", row);
        // 弹出确认警告提示框
        this.$confirm('此操作将永久删除该项目, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          // delete 和 post/patch方法的参数不一样，需要加一层data
          this.loading_flag = true;
          this.$api.deleteProject(row).then(resp => {
            this.loading_flag = false;
            if (resp['success']) {
              this.success(resp);
              this.getPagination(1);
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
            this.loading_flag = true;
            let obj;
            if (this.projectForm.id === '') {
              this.projectForm.file = this.$store.state.fileConent;
              obj = this.$api.addProject(this.projectForm);     // 没有就新建
            } else {
              obj = this.$api.updateProject(this.projectForm);  // 有就更新
            }
            // 给http response挂载一个处理的钩子
            obj.then(resp => {
              if (resp.success) {
                this.success(resp);
                this.getPagination(1);
              } else {
                this.failure(resp);
              }
              this.loading_flag = false;
              this.projectForm.name = '';
              this.projectForm.url = '';
              this.projectForm.file = "";
              this.$store.commit('setfileConent', "");
              this.setLocalValue("fileConent", "");
              this.projectForm.desc = '';
              this.projectForm.id = '';
            })
          } else {
            if (this.projectForm.id !== '') {
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
          duration: 30000
        });
      },
      getPagination(page) {
        this.$api.getProjectList({"owner": this.$store.state.user, "page": page}).then(resp => {
          if (resp["success"] === true) {
            this.projectData = resp.results;
            this.page = resp["page"];
            // this.success(resp);       // 弹出成功提示消息
          } else {
            // window.location.reload();
            this.$api.getProjectList({"owner": this.$store.state.user, "page": page}).then(resp => {
              if (resp["success"] === true) {
                this.projectData = resp.results;
                this.page = resp["page"];
                // this.success(resp);       // 弹出成功提示消息
              } else {
                this.failure(resp)
              }
            })
          }

        })
      }
    },
    mounted() {
      this.getPagination(1);
    },
    name: "ProjectList"
  }
</script>

<style scoped>
  .demo-table-expand {
    font-size: 0;
  }

  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
  }

  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  }
</style>
