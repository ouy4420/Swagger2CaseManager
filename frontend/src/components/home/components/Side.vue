<template>

  <el-menu
    class="common-side-bar"
    :default-active="$store.state.routerName"
    background-color="#0c0800"
    text-color="#BFCBD9"
    active-text-color="#318DF1"
    @select="select"
  >
    <el-menu-item index="ProjectList">
      <!--<i class="iconfont" >&#xe631;</i>-->
      项目列表
    </el-menu-item>

    <el-menu-item v-for="item of side_menu" :index="item.url" :key="item.url"
                  :disabled="$store.state.routerName === 'ProjectList'">
      <!--<span class="iconfont" v-html="item.code"></span>  -->
      {{item.name}}
    </el-menu-item>
  </el-menu>
</template>

<script>
  export default {
    name: "Side",
    data() {
      return {
        side_menu: [
          // {name: "项目概况", url: "ProjectDetail", code: "&#xe64a;"},
          {name: "测试用例", url: "AutoTest", code: "&#xe6da;"},
          {name: "API 接口", url: "APIView", code: "&#xe74a;"},
          {name: "环境变量", url: "GlobalEnv", code: "&#xe692;"},
          {name: "驱动代码", url: "DebugTalk", code: "&#xe7ca;"},
          {name: "历史报告", url: "Reports", code: "&#xe66e;"},
          {name: "定时任务", url: "TimerTask", code: "&#xe66e;"},
          {name: "CI/CD", url: "CICD", code: "&#xe66e;"}
        ],
      }
    },
    methods: {
      select(url) {
        this.$router.push({name: url});
        this.$store.commit('setRouterName', url);
        this.setLocalValue("routerName", url);
      }
    }
  }
</script>

<style scoped>

  .common-side-bar {
    position: fixed;
    top: 48px;
    border-right: 1px solid #ddd;
    height: 100%;
    width: 150px;
    background-color: #fff;
    display: inline-block;
  }

  .el-menu-item {
    font-size: 20px;
  }
</style>
