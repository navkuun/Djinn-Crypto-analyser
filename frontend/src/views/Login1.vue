// Login page
<template>
  <div class="loginform card p-d-flex p-jc-center p-mt-5">
    <Toast position="bottom-left" />
    <!-- <Toast position="top-right" /> -->
    <!-- This is the Login form -->
    <form
      class="p-fluid p-shadow-6 p-px-5 p-py-2"
      :model="formLogin"
      @submit.prevent="login"
      style="width: 50rem"
    >
      <h2>Login to Djinn</h2>
      <span class="p-float-label p-field">
        <InputText
          type="email"
          id="email"
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
          toggleMask
          type="password"
        >
        </Password>
        <Label id="passwordLabel" for="password">Password</Label>
      </span>
      <br />
      <span class="p-buttonset">
        <Button
          class="p-button-success"
          label="Submit"
          type="submit"
          @click="login"
          icon="pi pi-check"
          iconPos="left"
          id="submit"
        >
        </Button>
        <Button
          label="Or register"
          icon="pi pi-sign-in"
          iconPos="left"
          id="register"
          @click="goToPage('register')"
          style="height: 100%"
        >
        </Button>
      </span>
    </form>
    <p>{{ errors }}</p>
  </div>
</template>

<script>
// import axios from "axios";
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
  methods: {
    goToPage(page) {
      this.$router.push("/" + page);
    },
    created() {
      ipcRenderer.send(
        "resize-window",
        400,
        410,
        false,
        "Login to Djinn",
        true
      );
    },
    async login() {
      const Form = {
        email: this.formLogin.email,
        password: this.formLogin.password,
      };
      if (Form.email === "admin@gmail.com" && Form.password === "admin123") {
        this.$cookies.set("jwt", "adminjwt");
        // this.$store.commit("logIn",);
        this.$router.push("/dashboard");
      } else {
        this.errors = "Wrong login information";
      }
      // await axios
      //   .post(`http://localhost:5000/login`, Form, {
      //     withCredentials: true,
      //   })
      //   .then((res) => {
      //     console.log(res.data);
      //     this.$cookies.set("jwt", res.data.access_token);
      //     this.$store.commit("logIn", res.data);
      //     this.$toast.add({
      //       serverity: "success",
      //       summary: res.data.message,
      //     });
      //     this.$router.push("/dashboard");
      //   })
      //   .catch(() => {
      //     // if (err.response.status === 400) {
      //     //   this.errors = err.response.data.message;
      //     // } else {
      //     this.$toast.add({
      //       severity: "error",
      //       summary: "Something went wrong... try again",
      //     });
      //   });
    },
  },
};
</script>

<style>
/* #submit {
  margin-bottom: 10px;
}
#register {
  margin-bottom: 10px;
}
#email {
  margin-bottom: 15px;
} */
</style>