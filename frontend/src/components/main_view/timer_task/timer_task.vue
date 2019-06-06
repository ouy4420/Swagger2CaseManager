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

  </el-container>
</template>

<script>

  export default {
    components: {},
    data() {
      return {
        projectInfo: {
          "name": "---",
          "desc": "---"
        }
      }
    },
    methods: {

    },
    mounted() {
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
