<template>
<div>
  <div>
        <div style="padding: 10px; text-align: right;">
          <el-button style="margin-left: 50px"
                     type="info"
                     round
                     size="small"
                     icon="el-icon-d-arrow-left"
                     :disabled="apiData.previous === null "
                     @click="getPagination_api(apiData.previous)"
          >
            上一页
          </el-button>

          <el-button type="info"
                     round
                     size="small"
                     :disabled="apiData.next === null"
                     @click="getPagination_api(apiData.next)"
          >
            下一页
            <i class="el-icon-d-arrow-right"></i>
          </el-button>
        </div>
      </div>
  <api_list></api_list>
</div>

</template>

<script>
  import APIList from "./APIList"
  export default {
    name: "APIList",
    components:{
      "api_list": APIList
    },
    data() {
      return {
        apiData: {
          "previous": 0,
          "now": 1,
          "next": 2
        }
      }
    },
    methods: {
      getPagination_api(page) {
        const project_id = this.$route.params.id;
        this.$api.getPagination({"id": project_id, "page": page}).then(resp => {
          this.apiData = resp;
        })
      }
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
