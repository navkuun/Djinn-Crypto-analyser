<template>
  <router-view :key="$route.fullPath" @refreshData="refresh" />
</template>

<script>
import axios from "axios";
// import Login from "./views/Login.vue";
// import LandingPage from "./views/LandingPage.vue";

export default {
  name: "App",
  // components: {
  //   Login,
  //   LandingPage,
  // },
  data() {
    return {};
  },
  watch: {
    $route() {
      this.refresh();
    },
  },
  created() {
    document.body.style.zoom = "75%";
  },
  mounted() {
    this.refresh();
  },
  methods: {
    /*
     * User authorization check that is being called by emmit event
     * - refreshDAta everytime user changes a route.
     */
    async refresh() {
      // ----
      if (
        !this.$cookies.get("jwt") &&
        location.href.substring(location.href.lastIndexOf("/") + 1) !==
          "register"
      ) {
        this.$router.push("/");
        axios.defaults.headers.common["Authorization"] = null;
      } else if (
        !this.$cookies.get("jwt") &&
        location.href.substring(location.href.lastIndexOf("/") + 1) ===
          "register"
      ) {
        axios.defaults.headers.common["Authorization"] = null;
      } else {
        axios.defaults.headers.common[
          "Authorization"
        ] = `bearer ${this.$cookies.get("jwt")}`;
      }
      // to stop going back to login page
      if (
        this.$cookies.get("jwt") &&
        location.href.substring(location.href.lastIndexOf("/") + 1) === ""
      ) {
        this.$router.push("/dashboard");
      } else if (
        this.$cookies.get("jwt") &&
        location.href.substring(location.href.lastIndexOf("/") + 1) ===
          "register"
      ) {
        this.$router.push("/dashboard");
      } else if (
        this.$cookies.get("jwt") &&
        location.href.substring(location.href.lastIndexOf("/") + 1) === "login"
      ) {
        this.$router.push("/dashboard");
      }
      // ------
    },
  },
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
body {
  background-color: white;
  color: black;
}
</style>
