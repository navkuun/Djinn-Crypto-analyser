<template>
  <div>
    <preloader />
    <h1>This is the results page</h1>
    <Button
      @click="this.$router.go(-1)"
      icon="pi pi-arrow-left"
      label="Go back"
      class="p-button-outlined p-button-rounded p-shadow-3"
    />
    testing {{ crypto_data }}
  </div>
</template>

<script>
import Preloader from "../components/Preloader.vue";
export default {
  componetns: { Preloader },
  data() {
    return {
      crypto_data: null,
    };
  },
  async created() {
    this.crypto_data = localStorage.getItem("crypto_data");
  },
};
</script>
