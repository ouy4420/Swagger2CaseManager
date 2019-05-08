<template>
  <el-container>

    <el-header
    v-loading="loading_flag"
    element-loading-text="报告拼命加载中，请稍侯">
      <ul class="title-project">
        <li class="title-li" title="Test Project">
          <b>{{projectInfo.name}}</b>
          <b class="desc-li">{{projectInfo.desc}}</b>
        </li>
      </ul>
    </el-header>
    <el-container style="margin-bottom: 20px">
      <el-aside style="width: 450px; margin-left:10px; margin-top: 40px; border: solid">
        <case_list @e-autotest="getData"></case_list>
      </el-aside>
      <el-main style="margin-left:10px; margin-top: 40px; margin-right: 20px; border: solid;">
        <case_content></case_content>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
  import CaseList from "./case_list/case_list"
  import CaseContent from "./case_content/case-content"

  export default {
    name: "CASEView",
    components: {
      "case_list": CaseList,
      "case_content": CaseContent
    },
    data() {
      return {
        loading_flag: false,
        projectInfo: {
          "name": "11",
          "desc": "22"
        }
      }
    },
    methods: {
      getProjectDetail() {
        console.log("step1");
        const project_id = this.$route.params.id;
        console.log("step2", project_id);
        this.$api.getProjectDetail(project_id).then(res => {
          console.log("step3", res);
          this.projectInfo = res
        })
      },
      getData(loading_flag) {
      this.loading_flag = loading_flag;
    }
    },

    mounted() {
      // console.log("step1");
      this.getProjectDetail()
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
