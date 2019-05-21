<template>
  <el-tree
    :data="data5"
    show-checkbox
    node-key="id"
    default-expand-all
    :expand-on-click-node="false">
      <span class="custom-tree-node" slot-scope="{ node, data }">
        <span>{{ node.label }}</span>

        <span>
           <el-button type="text"
                      icon="el-icon-edit"
                      @click="editCaseName"
           ></el-button>
          <el-button
            type="text"
            icon="el-icon-circle-plus"
            size="mini"
            @click="() => append(data)">
          </el-button>
          <el-button
            type="text"
            icon="el-icon-remove"
            size="mini"
            @click="() => remove(node, data)">
          </el-button>
        </span>
      </span>
  </el-tree>
</template>

<script>
  let id = 1000;

  export default {
    data() {
      const data = [{
        id: "key1",
        label: 'key1',
        children: [{
          id: "value1",
          label: 'value1',
          children: [{
            id: 9,
            label: '三级 1-1-1'
          }]
        }]

        }];
      return {
        data5: JSON.parse(JSON.stringify(data))
      }
    },

    methods: {
      append(data) {
        const newChild = {id: id++, label: 'testtest', children: []};
        if (!data.children) {
          this.$set(data, 'children', []);
        }
        data.children.push(newChild);
      },

      remove(node, data) {
        const parent = node.parent;
        const children = parent.data.children || parent.data;
        const index = children.findIndex(d => d.id === data.id);
        children.splice(index, 1);
      },
      editCaseName() {
        this.$prompt('请输入测试用例名称', '编辑用例名称', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          // inputPattern: /[^\u4e00-\u9fa5]+/,
          // inputErrorMessage: '请勿输入中文！！'
        }).then(({value}) => {
          // 提示成功消息
          this.$message({
            type: 'success',
            message: '新的用例名称是: ' + value
          });
          // 更新测试用例名称
          // this.updateConfig(value);
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消输入'
          });
        });
      },
    }
  };
</script>

<style>
  .custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 8px;
  }
</style>
