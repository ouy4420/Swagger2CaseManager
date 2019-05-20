<template>

  <div>
    <el-button
      type="success"
      icon="el-icon-circle-plus"
      size="small"
      style="margin-left: 20px"
      @click="handleAdd">新增API
    </el-button>
    <el-dialog
      :title="DialogTitle"
      :visible.sync="DialogVisible"
      width="30%"
      align="center"
      @close="reset_api_form"
    >
      <el-dialog
        width="46%"
        title="编辑Header"
        :visible.sync="innerVisible_headers"
        append-to-body>
        <headers :headers="apiForm.headers"  @set_header="get_header"></headers>
      </el-dialog>

      <el-dialog
        width="46%"
        title="编辑QueryString"
        :visible.sync="innerVisible_params"
        append-to-body>
        <params :params="apiForm.params" @set_params="get_params"></params>
      </el-dialog>
      <el-form :model="apiForm"
               :rules="rules"
               ref="apiForm"
               label-width="110px"
               class="project">
        <el-form-item label="API名称" prop="name">
          <el-input placeholder="请输入API名称" v-model="apiForm.name"></el-input>
        </el-form-item>
        <el-form-item label="API调用" prop="def">
          <el-input placeholder="格式：func() 或 func($data)" v-model="apiForm.def"></el-input>
        </el-form-item>
        <el-form-item label="请求地址" prop="key">
          <el-input placeholder="请输入请求地址" v-model="apiForm.url" clearable>
            <el-select v-model="apiForm.method" slot="prepend" placeholder="请求方法" style="width: 110px">
              <el-option label="GET" value="GET"></el-option>
              <el-option label="POST" value="POST"></el-option>
              <el-option label="PATCH" value="PATCH"></el-option>
              <el-option label="PUT" value="PUT"></el-option>
              <el-option label="DELETE" value="DELETE"></el-option>
              <el-option label="OPTIONS" value="OPTIONS"></el-option>
            </el-select>
          </el-input>
        </el-form-item>
        <el-form-item label="Body类型" prop="body_type">
          <el-input v-model="apiForm.body_type">
            <el-select v-model="apiForm.body_type" slot="prepend" placeholder="Body类型" style="width: 110px">
              <el-option label="Json" value="Json"></el-option>
              <el-option label="Form" value="Form"></el-option>
              <el-option label="Null" value="Null"></el-option>
            </el-select>
          </el-input>
        </el-form-item>
        <el-form-item label="QuerString" prop="params">
          <!--<el-input :placeholder="quert_string_format" type="textarea" v-model="apiForm.params"></el-input>-->
          <i class="el-icon-edit-outline" @click="innerVisible_params=true"></i>
        </el-form-item>

        <el-form-item label="请求Headers" prop="headers">
          <!--<el-input placeholder="输入格式：json" type="textarea" v-model="apiForm.headers"></el-input>-->
          <i class="el-icon-edit-outline" @click="innerVisible_headers=true"></i>
        </el-form-item>

      </el-form>
      <span slot="footer" class="dialog-footer">
                        <el-button @click="DialogVisible = false">取消</el-button>
                        <el-button type="primary" @click="handleConfirm()">确 定</el-button>
                      </span>
    </el-dialog>
    <el-table
      :data="apiList"
      style="width: 100%;">

      <el-table-column type="expand">
        <template slot-scope="props">
          <el-form label-position="left" inline class="demo-table-expand">
            <el-form-item label="API调用: ">
              <span>{{ props.row.defname }}</span>
            </el-form-item>
            <el-form-item label="API名称: ">
              <span>{{ props.row.name }}</span>
            </el-form-item>
            <el-form-item label="URL: ">
              <span>{{ props.row.url }}</span>
            </el-form-item>
            <el-form-item label="Method: ">
              <span>{{ props.row.method }}</span>
            </el-form-item>
            <el-form-item label="Headers: ">
              <ul>
                <li v-for="(val, key) in props.row.headers">
                  <span>{{ key + ":" }}</span>
                  <span>{{ val }}</span>
                </li>
              </ul>

            </el-form-item>
            <el-form-item label="Params: ">
              <ul>
                <li v-for="(val, key) in props.row.params">
                  <span>{{ key + ":" }}</span>
                  <span>{{ val }}</span>
                </li>
              </ul>
            </el-form-item>
            <el-form-item label="json: ">
              <span>{{ props.row.json }}</span>
            </el-form-item>
            <el-form-item label="data: ">
              <span>{{ props.row.data }}</span>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>

      <el-table-column
        label="Index"
        prop="index">
      </el-table-column>
      <el-table-column
        label="Name"
        prop="name">
      </el-table-column>
      <el-table-column
        label="URL"
        prop="url">
      </el-table-column>
      <el-table-column
        label="Method"
        prop="method">
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
  import Headers from "./headers/headers"
  import Params from "./params/params"
  export default {
    name: "APIList",
    props: ["apiList"],
    components: {
      headers: Headers,
      params: Params,
    },
    data() {
      return {
        innerVisible_headers: false,
        innerVisible_params: false,
        DialogTitle: "",
        DialogVisible: false,
        APIListData: [],
        apiForm: {
          id: '',
          name: '',
          def: '',
          method: '',
          url: '',
          params: [{key: "", value: ""}],
          // headers: JSON.stringify({"content-type": "application/json"}, null, 2),
          headers: [{key: "content-type", value: "application/json"}],
          body_type: ''
        },
        quert_string_format: "输入格式：json 如：\n" + JSON.stringify({"aa": "111", "bb": "222"}, null, 2),
        rules: {
          name: [
            {required: true, message: '请输入API名称', trigger: 'blur'},
            {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
          ],
          def: [
            {required: true, message: '请输入API调用', trigger: 'blur'},
            {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
          ],
          url: [
            {required: true, message: '请输入url', trigger: 'blur'},
            {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
          ],
          body_type: [
            {required: true, message: '请输入body类型', trigger: 'blur'},
            {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
          ]
        }
      }
    },
    methods: {
      get_header(headers){
        this.innerVisible_headers = false;
        this.apiForm.headers = JSON.stringify(headers, null, 2);
      },
       get_params(params){
        this.innerVisible_params = false;
        this.apiForm.params = JSON.stringify(params, null, 2);
        console.log(params)
      },
      handleAdd() {
        this.DialogVisible = true;           // 弹出添加框
        this.DialogTitle = '添加API'     // 设置dialog title
      },
      handleEdit(index, row) {
        this.DialogVisible = true;           // 弹出编辑框
        this.DialogTitle = '编辑API';  // 设置dialog title
        console.log("row: ", row)
        // 显示要编辑的数据 ---------------------------------------
        this.apiForm.name = row['name'];
        this.apiForm.def = row['defname'];
        this.apiForm.method = row['method'];
        this.apiForm.url = row["url"];
        this.apiForm.params = JSON.stringify(row["params"], null, 2);
        this.apiForm.headers = JSON.stringify(row["headers"], null, 2);
        this.apiForm.id = row['id'];
        this.apiForm.body_type = row['body_type'];
      },
      handleDelete(index, row) {
        // 弹出确认警告提示框
        this.$confirm('此操作将永久删除该API, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          // delete 和 post/patch方法的参数不一样，需要加一层data
          this.$api.deleteAPI({"api_id": row.id}).then(resp => {
            if (resp['success']) {
              this.success(resp);       // 弹出成功提示消息
              this.$emit('refresh', true);          // 重新刷新当前api数据
            } else {
              this.failure(resp);
            }
            this.reset_api_form()  // 重置表单数据
          })
        })
      },
      reset_api_form() {
        this.apiForm = {
          id: '',
          name: '',
          def: '',
          method: '',
          url: '',
          params: [{key: "", value: ""}],
          // headers: JSON.stringify({"content-type": "application/json"}, null, 2),
          headers: [{key: "content-type", value: "application/json"}],
          body_type: ''
        };
      },
      handleConfirm() {
        this.$refs["apiForm"].validate((valid) => {
            if (valid) {
              if (this.apiForm["def"].indexOf("$data") < 0 && this.apiForm["body_type"] !== "Null") {
                this.$alert('请选择正确的Body类型！', '注意', {
                  confirmButtonText: '确定',
                  callback: action => {
                  }
                });
                return
              }

              this.DialogVisible = false;  // 新建或编辑框中的数据校验通过后，将弹框隐藏掉
              let obj;
              if (this.apiForm.id === '') {
                // 没有就新建
                this.apiForm.project_id = this.$route.params.id;
                obj = this.$api.addAPI({"api_obj": this.apiForm});
              } else {
                // 有就更新
                obj = this.$api.updateAPI({"api_obj": this.apiForm});
              }
              // 给http response挂载一个处理的钩子
              obj.then(resp => {
                if (resp.success) {
                  this.success(resp);       // 弹出成功提示消息
                  this.$emit('refresh', true);          // 重新刷新当前api数据
                } else {
                  this.failure(resp);
                }
                this.reset_api_form()  // 重置表单数据
              })
            } else {
              this.DialogVisible = true;
              if (this.apiForm.id !== '') {
                this.DialogTitle = "编辑API";  // 已经存在显示编辑框
              } else {
                this.DialogTitle = "新增API";  // 不存在显示新建框
              }
              return false;
            }
          }
        );

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
      },
    },
    mounted() {

    }
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
