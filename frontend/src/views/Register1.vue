<template>
  <div class="registerForm card p-d-flex p-jc-center p-mt-5">
    <form
      class="p-fluid p-shadow-6 p-px-5 p-py-2"
      style="width: 50rem"
      @submit.prevent="login"
    >
      <h2>Register | tmua-trainer</h2>
      <span class="p-float-label p-field">
        <InputText
          type="text"
          id="username"
          v-model="formRegister.username"
          autofocus
          required
        >
        </InputText>
        <Label for="username"> Username </Label>
      </span>
      <br />
      <span class="p-float-label p-field">
        <Password required toggleMask v-model="formRegister.password"
          ><template #footer>
            <hr />
            <p class="p-mt-2"><b> Suggestions: </b></p>
            <ul class="p-pl-2 p-ml-2 p-mt-0" style="line-height: 1.5">
              <li>At least one lowercase</li>
              <li>At least one uppercase</li>
              <li>At least one number</li>
              <!-- <li>Minimum 8 characters</li> -->
            </ul>
          </template>
        </Password>
        <Label id="passwordLabel" for="password">Password</Label>
      </span>
      <br />
      <span class="p-float-label p-field">
        <InputText
          required
          type="email"
          id="email"
          v-model="formRegister.email"
        >
        </InputText>
        <Label id="emailLabel" for="email">Email</Label>
      </span>

      <Button
        class="p-button-success"
        label="Submit"
        type="submit"
        @click="register"
        icon="pi pi-check"
        iconPos="left"
        id="submit"
      >
      </Button>
      <Button
        label="Or Login"
        @click="goToPage('')"
        icon="pi pi-sign-in"
        iconPos="left"
        id="Login"
      >
      </Button>
      <!-- <Button
        @click="goToPage('')"
        label="Home"
        icon="pi pi-home"
        iconPos="left"
      >
      </Button> -->
      <p>
        <i> {{ errors }} </i>
      </p>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      formRegister: {
        username: null,
        password: null,
        email: null,
      },
      errors: null,
    };
  },
  methods: {
    goToPage(page) {
      this.$router.push("/" + page);
    },
    isEmailValid: function () {
      return this.formInline.email == ""
        ? ""
        : this.formInline.reg.test(this.formInline.email)
        ? true
        : false;
    },

    validateRegister(email) {
      this.$refs[email].validate((valid) => {
        if (valid) {
          this.isEmailValid();
          if (this.isEmailValid() === true) {
            this.register();
          } else {
            return false;
          }
        } else {
          return false;
        }
      });
    },
    async register() {
      const Form = {
        username: this.formRegister.username,
        password: this.formRegister.password,
        email: this.formRegister.email,
      };
      console.log(Form);
      await axios
        .post(`http://localhost:5000/register`, Form, {
          withCredentials: true,
        })
        .then((res) => {
          console.log(res);

          this.$router.push("/dashboard");
        })
        .catch((err) => {
          if (err.response.status === 400) {
            this.errors = err.response.data.message;
          } else {
            this.errors =
              "Something went wrong...did you put in the correct info?";
          }
        });
    },
  },
};
</script>

<style>
#submit {
  margin-bottom: 10px;
}
#Login {
  margin-bottom: 10px;
}
</style>