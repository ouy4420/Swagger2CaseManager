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
            width="200"
            align="center"
          >
            <template slot-scope="scope">
              <span>{{ scope.row.current_time }}</span>
            </template>
          </el-table-column>
          <el-table-column
            label="测试人员"
            width="200"
            align="center"
          >
            <template slot-scope="scope">
              <span>{{ scope.row.tester }}</span>
            </template>
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
        projectInfo: {
          "name": "11",
          "desc": 22
        },
        page: {
          page_now: 1,
          page_previous: null,
          page_next: 2
        },
        reportList: []
      }
    },
    methods: {
      handleDelete(index, row) {
        // 弹出确认警告提示框
        this.$confirm('此操作将永久删除该项目, 是否继续?', '提示', {
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
          duration: 1000
        });
      },
      failure(resp) {
        this.$notify.error({
          message: resp["msg"],
          duration: 1000
        });
      },
      getPagination(page) {
        const project_id = this.$route.params.id;
        this.$api.getPagination_report({"id": project_id, "page": page}).then(resp => {
            this.reportList = resp["reportList"];
            this.projectInfo = resp["projectInfo"];
            this.page = resp["page"];
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
        inputPattern: /[^\u4e00-\u9fa5]+/,
        inputErrorMessage: '请勿输入中文！！'
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
    }
    },
    mounted() {
      this.getPagination(1);
    }
  }
</script>

<style scoped>
  .title-project {
    margin-top: 40px;
    margin-left: 10px;
  }

  ul li {
    list-style: none;
  }

  .title-li {
    font-size: 24px;
    color: #607d8b;
  }

  .desc-li {
    margin-top: 10px;
    color: #b6b6b6;
    font-size: 14px;
  }
</style>
