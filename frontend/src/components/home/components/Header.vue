<template>
  <div>
    <div class="nav-header">
      <div class="logo">
          <img src="./logo.png" alt="维基链">
          <span>WaykiChain -</span>
          <span class="devolepping">接口自动化测试平台</span>
      </div>
      <!--<img src="https://www.wiccdev.org/images/index/logo.png" alt="" style="width: 50px; height: 50px;">-->
      <!--<span style="color: white; font-size: 25px; margin-left: 10px">维基链 - 接口自动化测试平台</span>-->
      <span class="right">
                <div style="float: right; color: #d9d9d9; margin-right: 100px">
                    <span v-text="this.$store.state.user" style="padding-left: 5px; font-size: large"></span>
                    <a style="padding-left: 10px;" @click="handleLogOut">注 销</a>
                </div>
            </span>

    </div>
  </div>


</template>

<script>

  export default {
    methods: {
      handleLogOut() {
        this.$store.commit("isLogin", null);
        this.setLocalValue("token", null);
        this.$router.push({name: "Login"});
      }
    },
    name: "Header",

  }
</script>

<style scoped>
  .right {
    position: fixed;
    left: 300px;
    right: 0;
    top: 0;

  }

  .right div a:hover {
    color: darkcyan;
  }

  .nav-header {
    position: fixed;
    z-index: 666666;
    background: #077bf3;
    margin: 0 auto;
    font-size: 14px;
    width: 100%;
    border-bottom: 1px solid #ddd;
    height: 49px;
    line-height: 49px;
  }


  .logo a {
    display: block;
    text-decoration: none;
  }

  .logo img {
    width: 44px;
    margin-bottom: -15px;
  }

  .logo span {
    margin-left: 8px;
    font-size: 20px;
    color: white;
  }

  .devolepping {
    font-size: 16px;
  }
</style>
