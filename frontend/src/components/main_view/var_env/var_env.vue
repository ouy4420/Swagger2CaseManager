<template>
  <el-container>
    <el-header style="margin-bottom: 20px">
      <ul class="title-project">
        <li class="title-li" title="Test Project">
          <b>{{projectInfo.name}}</b>
          <b class="desc-li">{{projectInfo.desc}}</b>
        </li>
      </ul>
    </el-header>

    <base_url :BaseURLList="BaseURLList" @refresh="refresh"></base_url>
    <div style="margin-bottom: 50px"></div>
    <variabels :var_envList="var_envList" :page="page" @refresh="refresh"></variabels>

  </el-container>
</template>

<script>
  import BaseURL from './base_url/base_url'
  import Variables from './variables/variables'

  export default {
    components: {
      base_url: BaseURL,
      variabels: Variables
    },
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
        var_envList: [],
        BaseURLList: []
      }
    },
    methods: {
      refresh(refresh) {
        this.getPagination(1);
      },
      getPagination(page) {
        const project_id = this.$route.params.id;
        this.$api.getPagination_varenv({"id": project_id, "page": page}).then(resp => {
            this.var_envList = resp["var_envList"];
            this.projectInfo = resp["projectInfo"];
            this.page = resp["page"];
          }
        );
        this.$api.getBaseURLList({"project_id": project_id}).then(resp => {
            this.BaseURLList = resp["BaseURLList"];
          }
        );
      },
    },
    mounted() {
      this.getPagination(1);
    }
  }
</script>

<style scoped>

</style>
