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
        :selection="selectedNews"
        data-key="title"
        :metaKeySelection="false"
        height="400"
        responsiveLayout="scroll"
      >
        <template #header>
          <div>
            <Button
              icon="pi pi-external-link"
              label="Export Tweets statistics"
              @click="exportLink()"
            />
            <h2>Twitter news aggregator</h2>
          </div>
        </template>
        <Column selectionMode="multiple" headerStyle="width: 3em"></Column>
        <Column field="title" header="Tweet"> </Column>
        <Column field="source" header="User"> </Column>
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
      selectedTweet: null,
      newsOutlets: [
        {
          title: "Crypto to the moon!",
          source: "washington_post",
          rating: "2",
          sentiment: "0.5",
          trustworth: "7",
        },
        {
          title: "Elon buys twitter",
          source: "washington post",
          rating: "4",
          sentiment: "0.8",
          trustworth: "5",
        },
        {
          title: "Elon buys twitter",
          source: "washington post",
          rating: "4",
          sentiment: "0.8",
          trustworth: "5",
        },
        {
          title: "Elon buys twitter",
          source: "washington post",
          rating: "4",
          sentiment: "0.8",
          trustworth: "5",
        },
        {
          title: "Elon buys twitter",
          source: "washington post",
          rating: "4",
          sentiment: "0.8",
          trustworth: "5",
        },
      ],
    };
  },
  methods: {
    exportLink() {
      if (this.selectedTweet === null) {
        // Add error to toast
        this.$toast.add({
          severity: "error",
          detail: "You have to select a tweet!",
          summary: "You didn't select a tweet!",
        });
      } else {
        // Open chome tabs with the links of the websites
        this.$toast.add({
          severity: "info",
          summary: "Twitter pages should open soon...",
        });
      }
    },
  },
};
</script>