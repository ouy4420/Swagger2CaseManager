<template>

  <el-table
    :data="apiList"
    style="width: 100%;">

    <el-table-column type="expand">
      <template slot-scope="props">
        <el-form label-position="left" inline class="demo-table-expand">
          <el-form-item label="API调用: ">
            <span>{{ props.row.defname }}</span>
          </el-form-item>
          <el-form-item label="API名称: ">
            <span>{{ props.row.name }}</span>
          </el-form-item>
          <el-form-item label="URL: ">
            <span>{{ props.row.url }}</span>
          </el-form-item>
          <el-form-item label="Method: ">
            <span>{{ props.row.method }}</span>
          </el-form-item>
          <el-form-item label="Headers: ">
            <ul>
              <li v-for="(val, key) in props.row.headers">
                <span>{{ key + ":" }}</span>
                <span>{{ val }}</span>
              </li>
            </ul>

          </el-form-item>
          <el-form-item label="Params: ">
            <span>{{ props.row.params }}</span>
          </el-form-item>
          <el-form-item label="JsonData: ">
            <span>{{ props.row.jsondata }}</span>
          </el-form-item>
        </el-form>
      </template>
    </el-table-column>
    <el-table-column
      label="Index"
      prop="index">
    </el-table-column>
    <el-table-column
      label="Name"
      prop="name">
    </el-table-column>
    <el-table-column
      label="URL"
      prop="url">
    </el-table-column>
    <el-table-column
      label="Method"
      prop="method">
    </el-table-column>
  </el-table>

</template>

<script>
  export default {
    name: "APIList",
    props: ["apiList"],
    data() {
      return {
        APIListData: []
      }
    },
    methods: {
      success(resp) {
        this.$notify({
          message: resp["msg"],
          type: 'success',
          duration: 1000
        });
      },
      failure(resp) {
        this.$notify.error({
          message: resp.msg,
          duration: 1000
        });
      },
      // get_api_list() {
      //   const project_id = this.$route.params.id;
      //   this.$api.getAPIList({"id": project_id}).then(res => {
      //     console.log("res: ", res);
      //     this.APIListData = res
      //   })
      // }
    },
    mounted() {
      // this.get_api_list();
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
