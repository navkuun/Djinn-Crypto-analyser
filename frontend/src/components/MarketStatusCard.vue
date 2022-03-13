<template>
  <div>
    <Card id="market-card">
      <template #header> Market status </template>
      <template #content>
        <ProgressBar :value="value" />
      </template>
    </Card>
  </div>
</template>

<script>
// import axios from 'axios'
export default {
  data() {
    return {
      value: 50,
    };
  },
};
</script>

<style scoped>
#market-card {
  margin: 0 !important;
}
</style>
