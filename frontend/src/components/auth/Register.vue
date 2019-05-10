<template>
  <div>
    <div id="form-title" style="margin-top: 120px">维基链 - 接口测试平台</div>
    <el-form ref="regForm" :model="regForm" status-icon :rules="rules" label-width="80px" class="reg-form">
      <h2>用户注册</h2>
      <el-form-item label="用户名" prop="username">
        <el-input v-model="registerForm.username"></el-input>
        <div class="err_msg" id="user_err" v-html="usernameInvalid" @mouseover="usernameInvalid=''"></div>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input type="password" v-model="registerForm.password" auto-complete="off"></el-input>
        <div class="err_msg" id="pwd_err" v-html="passwordInvalid" @mouseover="passwordInvalid= ''"></div>
      </el-form-item>
      <el-form-item label="确认密码" prop="password_confirm">
        <el-input type="password" v-model="registerForm.repwd" auto-complete="off"></el-input>
        <div class="err_msg" id="repwd_err" v-html="repwdInvalid" @mouseover="repwdInvalid= ''"></div>
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="registerForm.email"></el-input>
        <div class="err_msg" id="email_err" v-html="emailInvalid" @mouseover="emailInvalid= ''"></div>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm">注册</el-button>
        <router-link to="/waykichain/login">已有账号？去登录</router-link>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
  export default {
    name: "Register",
    data() {
      return {
        registerForm: {
          username: '',
          password: '',
          repwd: '',
          email: ''
        },
        passwordInvalid: "",
        usernameInvalid: '',
        repwdInvalid: '',
        emailInvalid: ''
      };
    },
    methods: {
      validateUser() {
        const uPattern = /^[a-zA-Z0-9_-]{4,16}$/;
        if (!uPattern.test(this.registerForm.username)) {
          this.usernameInvalid = '用户名4到16位,只能是字母,数字,下划线,连字符';
          return false
        }
        return true
      },

      validatePassword() {
        const pPattern = /^[a-zA-Z\d_]{6,}$/;
        if (!pPattern.test(this.registerForm.password)) {
          this.passwordInvalid = "密码至少6位数";
          return false
        }
        return true
      },

      validateRepwd() {
        if (this.registerForm.password !== this.registerForm.repwd) {
          this.repwdInvalid = '确认密码和密码不一致';
          return false
        }
        return true
      },

      validateEmail() {
        const ePattern = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
        if (!ePattern.test(this.registerForm.email)) {
          this.emailInvalid = "邮箱格式不正确";
          return false
        }
        return true
      },

      submitForm() {
        if (this.validateUser() && this.validatePassword() && this.validateRepwd() && this.validateEmail()) {
          this.$api.register(this.registerForm).then(resp => {
            this.handleRegisterSuccess(resp)
          })
        }
      },

      handleRegisterSuccess(resp) {
        if (resp['success']) {
          this.$router.push('/waykichain/login/');  // 这里的this是？$router属性内容又是什么？
          this.$message.success({
            message: resp.msg,
            duration: 2000,
            center: true
          })
        } else {
          this.$message.error({
            message: resp["msg"],
            duration: 2000,
            center: true
          })
        }
      }
      ,
    }
  }
</script>

<style scoped>
  .reg-form {
    width: 400px;
    margin: 20px auto auto;
    padding: 20px;
    border: 1px solid #ddd;
  }

  .reg-form h2 {
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

  #form-title {
    font-size: 40px;
    color: #172B4D;
    text-align: center;
    margin-top: 60px;
  }
</style>
