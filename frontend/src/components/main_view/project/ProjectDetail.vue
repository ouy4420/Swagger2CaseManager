<template>
  <div>
    <ul class="title-project">
      <li class="title-li" title="Test Project">
        <b>{{projectInfo.name}}</b>
        <b class="desc-li">{{projectInfo.desc}}</b>
      </li>
    </ul>

    <el-carousel :interval="2000"
                 type="card"
                 height="300px"
                 style="margin-top: 80px; margin-left: 40px;margin-right: 40px">
      <el-carousel-item v-for="item in projectInfo.detail" >
        <div :id="item.desc"  class="detail" @click="trans_router(item.routerName)">
          <p class="title-p">{{item.length}}</p>
          <p class="desc-p">{{item.desc}}</p>
        </div>
      </el-carousel-item>
    </el-carousel>


  </div>
</template>

<script>
  export default {
    name: "ProjectDetail",
    data() {
      return {
        projectInfo: {}
      }
    },
    methods: {
      trans_router(routerName) {
        this.$store.commit('setRouterName', routerName);
        this.setLocalValue("routerName", routerName);
        this.$router.push({name: routerName});
      },
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
      getProjectDetail() {
        const project_id = this.$route.params.id;
        this.$api.getProjectDetail(project_id).then(res => {
          this.projectInfo = res
        })
      }
    },
    mounted() {
      this.getProjectDetail();
    }
  }
</script>

<style scoped>
  .detail{
    width: 800px;
    height: 800px;
    text-align: center;
  }

  .title-p {
    font-size: 50px;
    color: #607d8b;
  }

  .desc-p {
    color: #b6b6b6;
    font-size: 40px;
  }

  /*.el-carousel__item:nth-child(2n) {*/
    /*background-color: #67C23A;*/
  /*}*/

  /*.el-carousel__item:nth-child(2n+1) {*/
    /*background-color: #E6A23C;*/
  /*}*/


</style>
