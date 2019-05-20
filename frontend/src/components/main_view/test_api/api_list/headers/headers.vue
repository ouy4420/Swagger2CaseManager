<template>
  <div>
    <el-table
      highlight-current-row
      :data="headers"
      :height="height"
      style='width: 100%;'
      :border="false"
      @cell-mouse-enter="cellMouseEnter"
      @cell-mouse-leave="cellMouseLeave"
      :cell-style="{paddingTop: '4px', paddingBottom: '4px'}"
    >
      <el-table-column
        label="标签"
        width="300"
      >
        <template slot-scope="scope">
          <el-autocomplete
            clearable
            v-model="scope.row.key"
            :fetch-suggestions="keySearch"
            placeholder="头部标签"
          >
          </el-autocomplete>
        </template>
      </el-table-column>

      <el-table-column
        label="内容"
        width="400">
        <template slot-scope="scope">
          <el-autocomplete
            style="width: 380px;margin-right: 0px;"
            clearable
            v-model="scope.row.value"
            :fetch-suggestions="valueSearch"
            placeholder="头部内容"
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
      @click="set_header"
    >完成
    </el-button>
  </div>

</template>

<script>

  export default {
    props: {
      headers: {
        require: false
      }
    },
    methods: {
      set_header() {
        this.$emit('set_header', this.parseHeader(), this.headers);
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
        this.headers.push({
          key: '',
          value: ''
        });
      },

      handleDelete(index, row) {
        this.headers.splice(index, 1);
      },

      // 头部信息格式化
      parseHeader() {
        let header = {};
        for (let content of this.headers) {
          if (content['key'] !== '' && content['value'] !== '') {
            header[content['key']] = content['value'];
          }
        }
        return header;
      }
    },
    computed: {
      height() {
        return window.screen.height - 840
      }
    },
    data() {
      return {
        keyOptions: [{
          value: 'Authorization'
        }, {
          value: 'Cache-Control'
        }, {
          value: 'Connection'
        }, {
          value: 'Cookie'
        }, {
          value: 'Content-Type'
        }, {
          value: 'Host'
        }, {
          value: 'Origin'
        }, {
          value: 'Referer'
        }, {
          value: 'User-Agent'
        }],

        valueOptions: [{
          value: 'application/x-www-form-urlencoded'
        }, {
          value: 'text/xml'
        }, {
          value: 'application/json'
        }, {
          value: 'multipart/form-data'
        }],

        currentRow: ''
      }
    },
    name: "Header"
  }
</script>

<style scoped>
</style>
