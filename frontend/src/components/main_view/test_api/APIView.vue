<template>
  <div>
    <ul class="title-project">
      <li class="title-li" title="Test Project">
        <b>{{projectInfo.name}}</b>
        <b class="desc-li">{{projectInfo.desc}}</b>
      </li>
    </ul>
    <div>
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
    </div>
    <api_list :apiList="apiList"></api_list>
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
        apiList: []
      }
    },
    methods: {
      getPagination(page) {
        const project_id = this.$route.params.id;
        this.$api.getPagination_api({"id": project_id, "page": page}).then(resp => {
            this.apiList = resp["apiList"];
            this.projectInfo = resp["projectInfo"];
            this.page = resp["page"];
          }
        )
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
