<template>
  <el-container>
    <el-header>
      <ul class="title-project">
        <li class="title-li" title="Test Project">
          <b>{{projectInfo.name}}</b>
          <b class="desc-li">{{projectInfo.desc}}</b>
        </li>
      </ul>
    </el-header>
    <el-dialog
      title="邮件发送"
      :visible.sync="DialogVisible"
      width="30%"
      align="center"
      @close="reset_mail_form"
    >
      <el-form :model="mailForm"
               :rules="rules"
               ref="mailForm"
               label-width="110px"
               class="project">
        <el-form-item label="发送方邮箱" prop="from">
          <el-input placeholder="请输入发送方邮箱" v-model="mailForm.from"></el-input>
        </el-form-item>
        <el-form-item label="邮箱密码" prop="password">
          <el-input placeholder="请输入密码" v-model="mailForm.password" show-password></el-input>
        </el-form-item>
        <el-form-item label="接收方邮箱" prop="to">
          <el-autocomplete
            style="width: 425px"
            popper-class="my-autocomplete"
            v-model="mailForm.to"
            :fetch-suggestions="querySearch"
            placeholder="请输入发送方"
            @select="handleSelect">
            <i
              class="el-icon-edit el-input__icon"
              slot="suffix"
              @click="handleIconClick">
            </i>
            <template slot-scope="{ item }">
              <div>{{ item.value }}</div>
            </template>
          </el-autocomplete>

        </el-form-item>
        <el-form-item label="抄送" prop="more">
          <el-input placeholder="多个抄送方，请以分号隔开" v-model="mailForm.more"></el-input>
        </el-form-item>
        <el-form-item label="邮件描述" prop="description">
          <el-input type="textarea" placeholder="请输入邮件描述" v-model="mailForm.description"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
                        <el-button @click="DialogVisible = false">取消</el-button>
                        <el-button type="primary" @click="sendmail()">确 定</el-button>
                      </span>
    </el-dialog>

    <el-container>
      <el-main style="padding: 0; margin-top: 80px;margin-left: 10px; margin-right: 10px">
        <el-table
          highlight-current-row
          :data="reportList"
          border
          stripe
          :show-header="reportList.length > 0"
          style="width: 100%;"
        >
          <el-table-column
            label="编号"
            width="50"
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
            label="报告名称"
            width="200"
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
            label="生成时间"
            width="160"
            align="center"
          >
            <template slot-scope="scope">
              <span>{{ scope.row.current_time }}</span>
            </template>
          </el-table-column>
          <el-table-column
            label="测试人员"
            width="100"
            align="center"
          >
            <template slot-scope="scope">
              <span>{{ scope.row.tester }}</span>
            </template>
          </el-table-column>
          <el-table-column label="报告统计">
            <el-table-column
              prop="testsRun"
              label="testsRun"
              width="85">
            </el-table-column>
            <el-table-column
              prop="successes"
              label="successes"
              width="95">
            </el-table-column>
            <el-table-column
              prop="failures"
              label="failures"
              width="75">
            </el-table-column>
            <el-table-column
              prop="skipped"
              label="skipped"
              width="75">
            </el-table-column>
            <el-table-column
              prop="errors"
              label="errors"
              width="62">
            </el-table-column>
          </el-table-column>
          <el-table-column
            label="报告描述"
            width="400"
            align="center"
          >
            <template slot-scope="scope">
              <span>{{ scope.row.description }}</span>
            </template>
          </el-table-column>
          <el-table-column
            label="操作"
            align="center"
          >
            <template slot-scope="scope">
              <el-button
                size="medium"
                type="info"
                icon="el-icon-edit"
                @click="editDescription(scope.$index, scope.row)">添加描述
              </el-button>
              <el-button
                size="medium"
                type="success"
                icon="el-icon-info"
                @click="openReport(scope.$index, scope.row)">查看
              </el-button>
              <el-button
                size="medium"
                type="warning"
                icon="el-icon-message"
                @click="get_report_info(scope.$index, scope.row)">邮件
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
      <el-footer>
        <div style="padding: 10px; text-align: right;">
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

          <el-button type="info"
                     round
                     size="small"
                     :disabled="page.page_next === null"
                     @click="getPagination(page.page_next)"
          >
            下一页
            <i class="el-icon-d-arrow-right"></i>
          </el-button>
        </div>
      </el-footer>
    </el-container>
  </el-container>
</template>

<script>

  export default {
    components: {},
    data() {
      return {
        DialogVisible: false,
        mailForm: {
          "report_id": "",
          "from": "",
          "password": "",
          "to": "",
          "more": "",
          "description": ""
        },
        projectInfo: {
          "name": "11",
          "desc": 22
        },
        page: {
          page_now: 1,
          page_previous: null,
          page_next: 2
        },
        reportList: [],
        mail_list: [
          {"value": "zhixiang.liu@waykichainhk.com"},
          {"value": "ning.shen@waykichainhk.com"},
          {"value": "shenshan.wang@waykichainhk.com"},
          {"value": "qian.tan@waykichainhk.com"},
          {"value": "linxin.jiang@waykichainhk.com"}
        ],
        rules: {
          from: [
            {required: true, message: '请输入邮件发送方', trigger: 'blur'},
            {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
          ],
          password: [
            {required: true, message: '请输入密码', trigger: 'blur'},
            {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
          ],
          to: [
            {required: true, message: '请输入邮件接收方', trigger: 'blur'},
            {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
          ],
          description: [
            {required: true, message: '请输入邮件描述', trigger: 'blur'},
            {min: 1, max: 1000, message: '最多不超过1000个字符', trigger: 'blur'}
          ]
        }
      }
    },
    methods: {
      get_report_info(index, row) {
        this.DialogVisible = true;
        this.mailForm.report_id = row.id
      },
      sendmail() {
        this.DialogVisible = false;
        this.$api.mailReport({"mail": this.mailForm, "id": this.mailForm.report_id}).then(resp => {
          if (resp['success']) {
            this.success(resp);
          } else {
            this.failure(resp);
          }
        });
        this.reset_mail_form();
      },
      reset_mail_form() {
        this.mailForm = {
          "report_id": "",
          "from": "",
          "password": "",
          "to": "",
          "more": "",
          "description": ""
        }
      },
      handleDelete(index, row) {
        // 弹出确认警告提示框
        this.$confirm('此操作将永久删除该报告, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          // delete 和 post/patch方法的参数不一样，需要加一层data
          this.$api.deleteReport(row.id).then(resp => {
            if (resp['success']) {
              this.success(resp);
              this.getPagination(1);
            } else {
              this.failure(resp);
            }
          })
        })
      },
      success(resp) {
        this.$notify({
          message: resp["msg"],
          type: 'success',
          duration: 2000
        });
      },
      failure(resp) {
        this.$alert(resp["msg"], 'Error', {
          confirmButtonText: '确定',
          callback: action => {

          }
        });
        // this.$notify.error({
        //   message: resp["msg"],
        //   duration: 2000
        // });
      },
      getPagination(page) {
        const project_id = this.$route.params.id;
        this.$api.getPagination_report({"id": project_id, "page": page, "owner": this.$store.state.user}).then(resp => {
            this.reportList = resp["reportList"];
            this.projectInfo = resp["projectInfo"];
            this.page = resp["page"];
            this.mailForm.from = resp["owner_email"]
          }
        )
      },
      openReport(index, row) {
        this.$api.getReportDetail(row.id).then(resp => {
            var newWin = window.open("", "_blank");
            newWin.document.write(resp.render_content)
          }
        )

      },
      updateReport(id, value) {
        this.$api.updateReport({"id": id, "description": value}).then(resp => {
          if (resp['success']) {
            this.success(resp);
            this.getPagination(1);
          } else {
            this.failure(resp);
          }
        })
      },
      editDescription(index, row) {
        this.$prompt('请输入报告描述信息', '编辑报告描述', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          // inputPattern: /[^\u4e00-\u9fa5]+/,
          // inputErrorMessage: '请勿输入中文！！'
        }).then(({value}) => {
          // 提示成功消息
          this.$message({
            type: 'success',
            message: '报告描述信息是: ' + value
          });
          // 更新测试用例名称
          this.updateReport(row.id, value);
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消输入'
          });
        });
      },
      querySearch(queryString, cb) {
        var restaurants = this.mail_list;
        var results = queryString ? restaurants.filter(this.createFilter(queryString)) : restaurants;
        // 调用 callback 返回建议列表的数据
        cb(results);
      },
      createFilter(queryString) {
        return (restaurant) => {
          return (restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
        };
      },
      handleSelect(item) {
        console.log(item);
      },
      handleIconClick(ev) {
        console.log(ev);
      }
    },
    mounted() {
      this.getPagination(1);
    }
  }
</script>

<style scoped>

  li {
    line-height: normal;
    padding: 7px;
  }


  .highlighted .addr {
    color: #ddd;
  }


</style>
