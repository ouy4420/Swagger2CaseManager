<template>
  <div>
    <el-table
      highlight-current-row
      :data="params"
      :height="height"
      style='width: 100%;'
      :border="false"
      @cell-mouse-enter="cellMouseEnter"
      @cell-mouse-leave="cellMouseLeave"
      :cell-style="{paddingTop: '4px', paddingBottom: '4px'}"
    >
      <el-table-column
        label="Key"
        width="300"
      >
        <template slot-scope="scope">
          <el-autocomplete
            clearable
            v-model="scope.row.key"
            :fetch-suggestions="keySearch"
            placeholder="key"
          >
          </el-autocomplete>
        </template>
      </el-table-column>

      <el-table-column
        label="Value"
        width="400">
        <template slot-scope="scope">
          <el-autocomplete
            style="width: 380px;margin-right: 0px;"
            clearable
            v-model="scope.row.value"
            :fetch-suggestions="valueSearch"
            placeholder="value"
          >
          </el-autocomplete>
        </template>
      </el-table-column>

      <el-table-column>
        <template slot-scope="scope">
          <el-row v-show="scope.row === currentRow">
            <el-button
              icon="el-icon-circle-plus-outline"
              size="mini"
              type="info"
              @click="handleEdit(scope.$index, scope.row)">
            </el-button>

            <el-button
              icon="el-icon-delete"
              size="mini"
              type="danger"
              v-show="scope.$index !== 0"
              @click="handleDelete(scope.$index, scope.row)">
            </el-button>
          </el-row>

        </template>
      </el-table-column>
    </el-table>
    <el-button
      style="text-align: right"
      type="success"
      plain
      @click="set_params"
    >完成
    </el-button>
  </div>

</template>

<script>

  export default {
    props: {
      params: {
        require: false
      }
    },
    methods: {
      set_params() {
        this.$emit('set_params', this.parsePamras(), this.params);
      },
      keySearch(queryString, cb) {
        let keyOptions = this.keyOptions;
        let results = queryString ? keyOptions.filter(this.createFilter(queryString)) : keyOptions;
        cb(results);
      },
      valueSearch(queryString, cb) {
        let valueOptions = this.valueOptions;
        let results = queryString ? valueOptions.filter(this.createFilter(queryString)) : valueOptions;
        cb(results);
      }
      ,
      createFilter(queryString) {
        return (headerOptions) => {
          return (headerOptions.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
        };
      },

      cellMouseEnter(row) {
        this.currentRow = row;
      },

      cellMouseLeave(row) {
        this.currentRow = '';
      },

      handleEdit(index, row) {
        this.params.push({
          key: '',
          value: ''
        });
      },

      handleDelete(index, row) {
        this.params.splice(index, 1);
      },

      // 头部信息格式化
      parsePamras() {
        let params = {};
        for (let content of this.params) {
          if (content['key'] !== '' && content['value'] !== '') {
            params[content['key']] = content['value'];
          }
        }
        return params;
      }
    },
    computed: {
      height() {
        return window.screen.height - 840
      }
    },
    data() {
      return {
        keyOptions: [],

        valueOptions: [],

        currentRow: ''
      }
    },
    name: "Params"
  }
</script>

<style scoped>
</style>
