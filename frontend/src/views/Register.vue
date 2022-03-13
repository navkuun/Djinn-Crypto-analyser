<template>
  <div>
    <img
      src="../assets/Djinn.png"
      alt="Tmua trainer"
      id="login-header"
      height="55"
    />
    <div id="div-card" class="animate__animated animate__slideInDown">
      <Card id="login-card" class="p-shadow-4">
        <template #title id="card-title-signup"> Sign up </template>
        <template #subtitle id="card-subtitle-signup">
          The top cryptocurrency analyser
        </template>
        <template #content>
          <form class="p-fluid p-m-1" @submit.prevent="login">
            <!-- <h2 style="color: white">Register | tmua-trainer</h2> -->
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
              <Password
                id="password"
                required
                toggleMask
                v-model="formRegister.password"
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
            <br />

            <Button
              class="p-button-info p-button-rounded"
              label="Sign up "
              type="submit"
              @click="register"
              id="submit"
            >
            </Button>
            <Divider
              align="center"
              class="p-p-0"
              style="margin: 0; margin-bottom: 12px"
            >
              or
            </Divider>
            <Button
              label="Sign up with Google"
              @click="goToPage('register')"
              class="p-button-rounded"
              icon="pi pi-google"
              id="register"
              disabled
            >
            </Button>
          </form>
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
        </template>
      </Card>
      <div class="animate__animated animate__fadeInUp">
        <div class="p-d-flex p-ai-center p-jc-center">
          <p>Already have an account?</p>
          <Button
            label="Sign in"
            @click="goToPage('login')"
            id="join-now"
            class="p-button-rounded p-button-text p-px-1 p-mx-1 p-my-0 p-py-0"
          >
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
const { ipcRenderer } = require("electron");
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
  created() {
    ipcRenderer.send("resize-window", 400, 720, false, "Login to Djinn", true);
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
      const newUser = {
        username: this.formRegister.username,
        password: this.formRegister.password,
        email: this.formRegister.email,
      };
      console.log(newUser);
      await axios
        .post(`http://localhost:5000/register`, newUser, {
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

<style scoped>
#submit {
  margin-bottom: 10px;
}
#Login {
  margin-bottom: 10px;
}
/* #email {
  margin-bottom: 10px;
} */
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
/* .p-inputtext {
  height: 55px;
  font-size: 20px !important;
} */
#password,
#username,
#email {
  height: 55px !important;
  font-weight: bold;
}
#card-title-signup {
  font-weight: 600 !important;
  font-size: 35px !important;
  color: black;
}
#card-subtitle-signup {
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
