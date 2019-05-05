<template>

<div>
    <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
    <el-tab-pane label="Name" name="name">
      {{haha}}
    </el-tab-pane>
    <el-tab-pane label="Parameters" name="parameters">
      配置管理
    </el-tab-pane>
    <el-tab-pane label="Request" name="request">
      角色管理
    </el-tab-pane>
    <el-tab-pane label="Variables" name="variales">
      定时任务补偿
    </el-tab-pane>
  </el-tabs>
</div>

</template>

<script>

  export default {
    name: "Config",
    data() {
      return {
        config: {},
        activeName: 'variales'
      }
    },
    methods: {
      handleClick(tab, event) {
          console.log(1,tab);
          console.log(2, event);
        }
    },
    mounted() {

    }
  }
</script>

<style scoped>

</style>
