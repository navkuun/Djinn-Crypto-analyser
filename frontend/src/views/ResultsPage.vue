<template>
  <div>
    <preloader />
    <Chart
      v-show="showChart"
      type="line"
      :data="basicData"
      :options="basicOptions"
    />
  </div>
</template>
<script>
import Preloader from "../components/Preloader.vue";
export default {
  components: { Preloader },
  data() {
    return {
      crypto_data: null,
      showChart: false,
      basicData: {
        labels: null,
        datasets: [
          {
            label: "Sentiments over time",
            data: null,
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
  methods: {},
  async created() {
    this.crypto_data = await localStorage.getItem("crypto-data");
    console.log(this.crypto_data);
    const dates = [];
    const values = [];
    for (const date in JSON.parse(this.crypto_data)) {
      dates.push(date);
      values.push(JSON.parse(this.crypto_data)[date]);
    }
    console.log(dates);
    console.log(values);
    this.basicData.datasets.data = values;
    this.basicData.labels = dates;
    this.showChart = true;
  },
};
</script>



