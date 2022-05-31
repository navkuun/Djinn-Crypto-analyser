// Login page
<template>
  <div id="login-body">
    <img src="../assets/Djinn.png" alt="Djinn" id="login-header" height="55" />
    <Toast />
    <!-- <Card class="loginform card p-d-flex p-jc-center p-mt-5" id="login-card"> -->
    <div id="div-card" class="animate__animated animate__slideInDown">
      <Card id="login-card" class="p-shadow-4">
        <template #title id="card-title-login"> Sign in </template>
        <template #subtitle id="card-subtitle-login">
          The top cryptocurrency analyser
        </template>
        <template #content>
          <form
            class="p-fluid p-m-1"
            :model="formLogin"
            @submit.prevent="login"
            id="form"
          >
            <!-- <h2 style="color: white">Login | tmua-trainer</h2> -->
            <span class="p-float-label p-field">
              <InputText
                type="text"
                id="username"
                v-model="formLogin.email"
                autofocus
                required
              >
              </InputText>
              <Label id="text" for="text">Email</Label>
            </span>
            <br />
            <span class="p-float-label p-field">
              <Password
                required
                v-model="formLogin.password"
                :feedback="false"
                toggleMask
                style="height: 55px !important"
                id="password"
              >
              </Password>
              <Label id="passwordLabel" for="password">Password</Label>
            </span>
            <br />
            <Button
              class="p-button-rounded"
              label="Sign in"
              type="submit"
              @click="login"
              id="submit"
            >
            </Button>
            <p>
              <i style="color: red"> {{ errors }} </i>
            </p>
          </form>
        </template>
      </Card>
      <div class="animate__animated animate__fadeInUp">
        <div class="p-d-flex p-ai-center p-jc-center">
          <p>New to Djinn?</p>
          <Button
            label="Join now"
            @click="goToPage('register')"
            id="join-now"
            class="p-button-rounded p-button-text p-px-1 p-mx-1 p-my-0 p-py-0"
          >
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script scoped>
import axios from "axios";
const { ipcRenderer } = require("electron");
export default {
  name: "Login",
  data() {
    return {
      formLogin: {
        email: null,
        password: null,
      },
      errors: null,
    };
  },
  created() {
    ipcRenderer.send("resize-window", 400, 720, false, "Login to Djinn", true);
  },
  methods: {
    goToPage(page) {
      this.$router.push("/" + page);
    },
    async login() {
      const user = {
        username: this.formLogin.email,
        password: this.formLogin.password,
      };
      if (user.username === "admin@gmail.com" && user.password === "admin123") {
        this.$toast.add({
          severity: "success",
          summary: "You have logged in!",
        });
        this.$cookies.set("jwt", "adminjwt");
        // this.$store.commit("logIn",);
        this.$router.push("/dashboard");
        return;
      }
      await axios
        .post(`http://localhost:5000/api/login`, user)
        .then((res) => {
          console.log(res);
          this.$cookies.set("jwt", res.data.access_token);
          this.$store.commit("logIn", res.data);
          this.$router.push("/dashboard");
        })
        .catch((err) => {
          if (err.response.status === 400) {
            this.errors = err.response.data.msg;
          } else {
            this.$toast.add({
              severity: "error",
              detail: err.response.data.msg,
              summary: "Something went wrong...try again",
              life: 2000,
            });
          }
        });
    },
  },
};
</script>

<style  >
#login-header {
  position: absolute;
  left: 0;
  top: 0;
}

#login-card {
  margin-top: 10vh;
  width: 390px;
}
#div-card {
  display: inline-block;
  justify-content: center;
  align-items: center;
}
#form {
  width: 100% !important;
}
#password,
#username {
  height: 55px !important;
  font-size: 20px !important;
}

#register,
#submit {
  height: 56px;
  font-weight: bold;
}
#card-title-login {
  font-weight: 600 !important;
  font-size: 35px !important;
  color: black;
}
#card-subtitle-login {
  color: black !important;
}
#footer {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 30px; /* Height of the footer */
}
#join-now:hover {
  text-decoration: underline;
}
</style>