<template>

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
    <el-table
      ref="multipleTable"
      :data="caseList"
      tooltip-effect="dark"
      style="width: 100%"
      @selection-change="handleSelectionChange">
      <el-table-column
        type="selection"
        width="50">
      </el-table-column>
      <el-table-column
        label="用例编号"
        width="100">
        <template slot-scope="scope">{{ scope.row.index }}</template>
      </el-table-column>
      <el-table-column
        prop="name"
        label="用例名称"
        width="240">
      </el-table-column>
    </el-table>
    <div style="margin-top: 20px">
      <el-button @click="toggleSelection(caseList)">选中该项目中所有测试用例</el-button>
      <el-button @click="toggleSelection()">取消选择</el-button>
    </div>
  </div>

</template>

<script>

  export default {
    name: "CASEList",
    data() {
      return {
        caseList: [],
        multipleSelection: [],
        page: {
          page_now: 1,
          page_previous: null,
          page_next: 2
        }
      }
    },
    methods: {
      toggleSelection(rows) {
        if (rows) {
          this.$refs.multipleTable.clearSelection();
          rows.forEach(row => {
            this.$refs.multipleTable.toggleRowSelection(row);
          });
        } else {
          this.$refs.multipleTable.clearSelection();
        }
      },
      handleSelectionChange(val) {
        console.log("val: ", val)
        this.multipleSelection = val;
      },
      getPagination(page) {
        const project_id = this.$route.params.id;
        this.$api.getPagination_case({"id": project_id, "page": page}).then(resp => {
          this.caseList = resp["caseList"];
          this.page = resp["page"];
        })
      }
    },
    mounted() {
            var obj = this;
            function temp_func(){
                obj.getPagination(1)
            }
            setTimeout(temp_func,500)
    }
  }
</script>

<style scoped>

</style>
