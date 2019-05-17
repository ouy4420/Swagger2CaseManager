<template>
  <el-container>
    <el-header style="background-color: #F7F7F7;; padding: 0; height: 50px;">
      <div style="padding-top: 10px; margin-left: 10px; ">
        <el-row>
          <el-col :span="15">
            <el-button
              type="success"
              icon="el-icon-check"
              @click="handleConfirm"
              size="small"
            >
              Save
            </el-button>

            <el-button
              icon="el-icon-caret-right"
              type="info"
              size="small"
              @click="handleRunCode"
            >
              Run
            </el-button>
          </el-col>
        </el-row>
      </div>
    </el-header>

    <el-container>
      <el-main style="padding: 0; margin-left: 10px">
        <el-row>
          <el-col :span="15">
            <editor
              v-model="content.code"
              @init="editorInit"
              lang="python"
              theme="eclipse"
              width="100%"
              :height="codeHeight"
              :options="{
                                 enableSnippets:true,
                                 enableBasicAutocompletion: true,
                                 enableLiveAutocompletion: true
                             }"
            >
            </editor>
          </el-col>

          <el-col :span="9">
            <editor
              v-model="resp.msg"
              lang="text"
              theme="monokai"
              width="100%"
              :height="codeHeight"
            >
            </editor>
          </el-col>
        </el-row>

      </el-main>
    </el-container>
  </el-container>

</template>

<script>
  export default {
    data() {
      return {
        codeHeight: 800,
        content: {
          code: '',
          id: ''
        },
        resp: {
          msg: ''
        }
      }
    },
    name: "DebugTalk",
    methods: {
      make_format(value) {
        console.log("value: ", typeof value);
        try {
          var a = value.slice(0,-1);
          a = JSON.stringify(a, null, 2);
          a = JSON.parse(a)
          var res = JSON.stringify(a, null, 2);
          return res
        } catch (err) {
          return value
        }
      },
      handleRunCode() {
        console.log("this.content.code: ", this.content.code)
        this.$api.runDebugtalk({"code": this.content.code}).then(resp => {
          this.resp.msg = this.make_format(resp.resp);
          this.$message.success(resp["msg"]);

        })
      },

      handleConfirm() {
        this.$api.updateDebugtalk({"code": this.content.code, "project_id": this.$route.params.id}).then(resp => {
          this.getDebugTalk();
          this.$message.success(resp["msg"]);

        })
      },
      editorInit() {
        require('brace/ext/language_tools');
        require('brace/mode/python');
        require('brace/theme/eclipse');
        require('brace/snippets/python');
      },
      getDebugTalk() {
        this.$api.getDebugtalk({"project_id": this.$route.params.id}).then(res => {
          this.content.code = res.code;
          this.content.id = res.id;
        })
      }
    },
    components: {
      editor: require('vue2-ace-editor')
    },
    mounted() {
      this.getDebugTalk();
      this.codeHeight = window.screen.height - 248;
    }
  }
</script>

<style scoped>
  .ace_editor {
    position: relative;
    overflow: hidden;
    font: 18px/normal 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', 'source-code-pro', monospace !important;
    direction: ltr;
    text-align: left;
    -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
  }
</style>
