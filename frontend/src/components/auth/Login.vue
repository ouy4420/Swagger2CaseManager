<template>
  <div>
    <div id="form-title" style="margin-top: 120px">维基链 - 接口测试平台</div>
    <el-form ref="loginForm" v-if="!isLogin" :model="loginForm" status-icon :rules="rules" label-width="80px"
             class="login-form">
      <h2>用户登录</h2>
      <el-form-item label="用户名" prop="username">
        <el-input v-model="loginForm.username"></el-input>
        <div class="err_msg" id="email_err" v-html="usernameInvalid" @mouseover="usernameInvalid=''"></div>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input type="password" v-model="loginForm.password" auto-complete="off"></el-input>
        <div class="err_msg" id="pwd_err" v-html="passwordInvalid" @mouseover="passwordInvalid= ''"></div>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm">登录</el-button>
        <router-link to="/waykichain/register">还没有账号？去注册</router-link>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>

  export default {
    name: "Login",

    data() {
      return {
        loginForm: {
          username: '',
          password: '',
        },
        usernameInvalid: '',
        passwordInvalid: ''
      };
    },

    methods: {
      validateUserName() {
        if (this.loginForm.username.replace(/(^\s*)/g, "") === '') {
          this.usernameInvalid = "用户名不能为空";
          return false;
        }
        return true
      },

      validatePassword() {
        if (this.loginForm.password.replace(/(^\s*)/g, "") === '') {
          this.passwordInvalid = "密码不能为空";
          return false;
        }
        return true;
      },

      submitForm() {
        if (this.validateUserName() && this.validatePassword()) {
          this.$api.login(this.loginForm).then(resp => {
            this.handleLoginSuccess(resp)
          })
        }
      },

      handleLoginSuccess(resp) {
        if (resp.success) {
          this.$router.push({name: 'ProjectList'}); // 路由跳转，是这需要这句？？

          this.$store.commit("isLogin", resp.token);
          this.$store.commit("setUser", resp.user);
          // 搞清楚这个store和下面三个setLocalValue是干啥的
          this.$store.commit("setRouterName", 'ProjectList');

          this.setLocalValue("token", resp.token);
          this.setLocalValue("user", resp.user);
          this.setLocalValue("routerName", 'ProjectList');

          this.$message.success({
            message: resp.msg,
            duration: 2000,
            center: true
          })
        } else {
          this.$message.error({
            message: resp.msg,
            duration: 2000,
            center: true
          })
        }
      },
    }
  }
</script>

<style scoped>
  .login-form {
    width: 400px;
    margin: 20px auto auto;
    padding: 20px;
    border: 1px solid #ddd;
  }

  .login-form h2 {
    font-size: 24px;
    text-align: center;
    margin: 30px 0;
  }

  .err_msg {
    position: relative;
    color: #fc4949;
    height: 20px;
    line-height: 20px;
  }

</style>
