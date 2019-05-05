<template>
  <el-upload :file-list="uploadFiles"
             drag
             action="https://jsonplaceholder.typicode.com/posts/"
             :auto-upload="false"
             :on-change="loadJsonFromFile">
    <i class="el-icon-upload"></i>
    <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
    <div class="el-upload__tip" slot="tip">只能上传swagger josn文件</div>
  </el-upload>
</template>

<script>
  export default {
    data() {
      return {
        uploadFilename: null,
        uploadFiles: []
      }
    },
    methods: {
      loadJsonFromFile(file, fileList) {
        this.uploadFilename = file.name;
        this.uploadFiles = fileList;
        var last_file = this.uploadFiles[this.uploadFiles.length - 1];
        this.uploadFiles = [last_file];
        this.loadJsonFromFileConfirmed(last_file);

      },
      loadJsonFromFileConfirmed(file) {
        console.log(this.uploadFiles);
        if (this.uploadFiles) {
          console.log(file.raw);
          let reader = new FileReader();
          reader.readAsText(file.raw);
          reader.onload = async (e) => {
            try {
              let document = JSON.parse(e.target.result);
              console.log(document);
              this.$store.commit('setfileConent', document);
              console.log("setfileContent: ", this.$store.state.fileConent)
              this.setLocalValue("fileConent", document);
            } catch (err) {
              console.log(`load JSON document from file error: ${err.message}`)
              // this.showSnackbar(`Load JSON document from file error: ${err.message}`, 4000)
            }
          }
          //
        }
      }
    },
    mounted() {

    }

  }
</script>

<style scoped>

</style>
