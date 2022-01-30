<template>
  <div>
    <Toast />
    <div class="card p-shadow-3 p-mt-3" style="height: 500px">
      <DataTable
        :value="newsOutlets"
        :scrollable="true"
        :lazy="true"
        scrollHeight="flex"
        style="calc(100vh - 800px)"
        v-model:selection="selectedNews"
        data-key="title"
        :metaKeySelection="false"
        responsiveLayout="scroll"
      >
        <template #header>
          <div>
            <Button
              icon="pi pi-external-link"
              label="Export links"
              @click="exportLink()"
            />
            <h2>Crypto outlet news aggregator</h2>
          </div>
        </template>
        <Column selectionMode="multiple" headerStyle="width: 3em"></Column>
        <Column field="title" header="Title"> </Column>
        <Column field="source" header="news source"> </Column>
        <Column field="rating" header="Rating"> </Column>
        <Column field="sentiment" header="Sentiment(0-1)"> </Column>
        <Column field="trustworth" header="trustworthiness(1-10)"> </Column>
      </DataTable>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedNews: null,
      newsOutlets: [
        {
          title: "Crypto to the moon!",
          source: "washington post",
          rating: "3",
          sentiment: "0.5",
          trustworth: "7",
        },
        {
          title: "Crypto to the moon btc etc car omg!",
          source: "Sunday news",
          rating: "3",
          sentiment: "0.5",
          trustworth: "7",
        },
        {
          title: "Crypto to the moondsfsd!",
          source: "washington post",
          rating: "3",
          sentiment: "0.5",
          trustworth: "7",
        },
        {
          title: "BTC to the moon!",
          source: "washington post",
          rating: "3",
          sentiment: "0.5",
          trustworth: "7",
        },
        {
          title: "ETH to the moon!",
          source: "washington post",
          rating: "3",
          sentiment: "0.5",
          trustworth: "7",
        },
        {
          title: "ARE to the moon!",
          source: "washington post",
          rating: "3",
          sentiment: "0.5",
          trustworth: "7",
        },
        {
          title: "BER to the moon!",
          source: "washington post",
          rating: "3",
          sentiment: "0.5",
          trustworth: "7",
        },
        {
          title: "OMG to the moon!",
          source: "washington post",
          rating: "3",
          sentiment: "0.5",
          trustworth: "7",
        },
      ],
    };
  },
  methods: {
    exportLink() {
      if (this.selectedNews === null) {
        // Add error to toast
        this.$toast.add({
          severity: "error",
          detail: "You have to select a link!",
          summary: "You didn't select a link!",
        });
      } else {
        // Open chome tabs with the links of the websites
        this.$toast.add({
          severity: "info",
          summary: "The news should open in your preferred browser soon...",
        });
      }
    },
  },
};
</script>