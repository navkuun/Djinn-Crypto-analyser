<template>
  <div id="app">
    <Chart
      ref="primeChart"
      type="line"
      :data="basicData"
      :options="basicOptions"
    />
  </div>
</template>

<script>
import Chart from "primevue/chart";

export default {
  name: "App",
  components: {
    Chart,
  },
  setup() {
    return {
      basicData: {
        labels: ["0", "10", "20", "30", "40", "50", "60"],
        datasets: [
          {
            label: "Aggregation of market price",
            data: [65, 59, 80, 81, 56, 55, 40],
            fill: false,
            borderColor: "#42A5F5",
            tension: 0.4,
          },
        ],
      },
      basicOptions: {
        plugins: {
          legend: {
            labels: {
              color: "#495057",
            },
          },
        },
        scales: {
          x: {
            ticks: {
              color: "#495057",
            },
            grid: {
              color: "#ebedef",
            },
          },
          y: {
            ticks: {
              color: "#495057",
            },
            grid: {
              color: "#ebedef",
            },
          },
        },
      },
    };
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
