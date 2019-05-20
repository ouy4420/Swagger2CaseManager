<template>
  <div>
    <ul class="title-project">
      <li class="title-li" title="Test Project">
        <b>{{projectInfo.name}}</b>
        <b class="desc-li">{{projectInfo.desc}}</b>
      </li>
    </ul>
    <div>

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
    </div>
    <api_list :apiList="apiList" @refresh="refresh_api_list"></api_list>
  </div>

</template>

<script>
  import APIList from "./api_list/APIList"


  export default {
    name: "APIView",
    components: {
      "api_list": APIList
    },
    data() {
      return {
        projectInfo: {
          "name": "",
          "desc": ""
        },
        page: {
          page_now: 1,
          page_previous: null,
          page_next: 2
        },
        apiList: [],
      }
    },
    methods: {
      refresh_api_list(refresh) {
        this.getPagination(1);
      },
      getPagination(page) {
        const project_id = this.$route.params.id;
        this.$api.getPagination_api({"id": project_id, "page": page}).then(resp => {
            if (resp.success) {
              this.apiList = resp["apiList"];
              this.projectInfo = resp["projectInfo"];
              this.page = resp["page"];
              this.success(resp);       // 弹出成功提示消息
            } else {
              // window.location.reload();
              this.$api.getPagination_api({"id": project_id, "page": page}).then(resp => {
                if (resp.success) {
                  this.apiList = resp["apiList"];
                  this.projectInfo = resp["projectInfo"];
                  this.page = resp["page"];
                  this.success(resp);       // 弹出成功提示消息
                } else {
                  this.failure(resp);
                }
              })
            }
          }
        )
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
      }
    },
    mounted() {
      this.getPagination(1);
    }
  }
</script>

<style scoped>

</style>
