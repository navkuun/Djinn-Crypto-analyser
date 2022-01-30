<template>
  <div style="color: white" class="animate__animated animate__slideInDown">
    <Menubar :model="items" id="navbar" class="p-shadow-6">
      <template #start>
        <img class="p-m-0 p-p-0" src="../assets/Djinn.png" height="50" />
      </template>
      <!-- <template #end>
        <Button
          icon="pi pi-cog"
          class="p-button-rounded p-button-outlined"
        ></Button>
      </template> -->
    </Menubar>
    <div class="p-grid">
      <div class="p-col-6">
        <!-- <div class="box">graph</div> -->
        <dashboard-graph> </dashboard-graph>
      </div>
      <div class="p-col-6">
        <!-- MAIN FORM  -->
        <Steps :model="stepItems" class="p-mt-2" :readonly="true" />
        <div
          id="mainform"
          style="background-color: black"
          class="p-px-2 p-py-1 p-mt-4"
        >
          <form
            class="p-fluid p-m-4"
            id="mainForm"
            @submit.prevent="openSubmitCriteria"
          >
            <h4 style="text-decoration: underline">Crypto analyser</h4>
            <!-- <h4>Main Form</h4> -->
            <!-- SELECT CRYPTOCURRENCIES  DROPDOWN-->
            <span class="p-field">
              <Dropdown
                v-model="selectedCryptocurrency"
                :options="cryptocurrencies"
                optionLabel="name"
                :filter="true"
                placeholder="Select cryptocurrency"
                :showClear="true"
              >
                <!-- DROPDOWN TEMPALTES -->
                <template #value="slotProps">
                  <div
                    class="crypto-item crypto-item-value"
                    v-if="slotProps.value"
                  >
                    <div>{{ slotProps.value.name }}</div>
                  </div>
                  <span v-else>
                    {{ slotProps.placeholder }}
                  </span>
                </template>
                <template #option="slotProps">
                  <div class="crypto-item">
                    <div>{{ slotProps.option.name }}</div>
                  </div>
                </template>
                <!-- DROPDOWN TEMPALTES -->
              </Dropdown>
            </span>
            <br />
            <!-- TIME RANGE  -->
            <span class="p-field">
              <Dropdown
                v-model="selectedTime"
                :options="timeRanges"
                optionLabel="name"
                optionValue="name"
                placeholder="Select time range"
              />
              <br />
              <span class="p-buttonset">
                <Button
                  class="p-button-info"
                  label="Criteria"
                  @click="openSubmitCriteria"
                >
                </Button>
              </span>
            </span>
          </form>
        </div>
        <!-- MAIN FORM -->
        <div class="box">
          <crypto-outlet-news> </crypto-outlet-news>
        </div>
      </div>
      <div class="p-col-6">
        <div class="p-grid">
          <div class="p-col-6">
            <market-status-card />
          </div>
          <div class="p-col-6">
            <top-reddit-servers />
          </div>
        </div>
      </div>
      <div class="p-col-6">
        <!-- <div class="box">Twitter news</div> -->
        <twitter-news />
      </div>
    </div>
    <Dialog
      id="criteriaDialog"
      header="Submit Criteria"
      v-model:visible="displaySubmit"
      class="p-fluid"
      maximizable="true"
    >
      <!-- Place select buttons for options here -->
      <!-- In the future these options will be gotten from the db -->
      <p class="p-m-0">There will be more options in the future</p>
      <Divider />
      <form class="p-fluid p-field" @submit.prevent="submitForm">
        <Label> Algorithm type: </Label>
        <Dropdown
          v-model="selectedCriteria1"
          :options="algorithmType"
          optionLabel="name"
          optionValue="name"
          placeholder="Select Algorithm type"
          required
        />
        <Divider />
        <span class="p-buttonset">
          <Button
            label="Cancel"
            icon="pi pi-times"
            class="p-button-danger"
            @click="displaySubmit = false"
          />
          <Button
            label="Submit"
            type="submit"
            icon="pi pi-times"
            class="p-button-primary p-button-raised"
          />
        </span>
      </form>
    </Dialog>
  </div>
</template>

<script>
import TwitterNews from "../components/TwitterNews.vue";
import MarketStatusCard from "../components/MarketStatusCard.vue";
import TopRedditServers from "../components/TopRedditServers.vue";
// @ is an alias to /src
const { ipcRenderer } = require("electron");
const axios = require("axios");
const { default: DashboardGraph } = require("../components/dashboardGraph.vue");
const {
  default: CryptoOutletNews,
} = require("../components/CryptoOutletNews.vue");
export default {
  components: {
    DashboardGraph,
    CryptoOutletNews,
    TwitterNews,
    MarketStatusCard,
    TopRedditServers,
  },
  data() {
    return {
      stepItems: [
        { label: "Select crypto and time range", to: "/dashboard" },
        { label: "Choose options" },
        { label: "Visualizations and Key statistics", to: "/results-page" },
      ],
      displaySubmit: false,
      selectedTime: null,
      selectedCriteria1: null,
      algorithmType: [{ name: "Naive bayes" }, { name: "Logistic regression" }],
      timeRanges: [
        { name: "1 week" },
        { name: "2 week" },
        { name: "3 week" },
        { name: "1 month" },
      ],
      selectedCryptocurrency: null,
      cryptocurrencies: [
        // in the future maybe change names to $BTC-bitcoin
        { name: "Bitcoin" },
        { name: "Dogecoin" },
        { name: "Etherium" },
        { name: "ShibaInu" },
      ], // change this to fetch from db later
      items: [
        // {
        //   label: "logout",
        //   icon: "pi pi-fw pi-user",
        //   command: () => this.logout(),
        // },
        {
          label: "Settings",
          icon: "pi pi-fw pi-cog",
          items: [
            {
              label: "logout",
              icon: "pi pi-fw pi-sign-out",
              command: () => this.logout(),
            },
            {
              label: "account",
              icon: "pi pi-fw pi-user",
              to: "account-settings",
            },
          ],
        },
      ],
    };
  },
  methods: {
    async logout() {
      this.$store.commit("logOut");
      this.$cookies.remove("jwt");
      axios.defaults.headers.common["Authorization"] = null;
      this.$router.push("/");
    },
    openSubmitCriteria() {
      this.displaySubmit = true;
    },
    submitForm() {
      this.$router.push("/results-page");
    },
  },
  computed: {},
  created() {
    ipcRenderer.send("resize-window-main", 1600, 900, true, "Dashboard", true);
  },
  async mounted() {
    await axios
      .get("http://localhost:5000/test")
      .then((res) => {
        this.name = res;
      })
      .catch(() => {
        this.name = `sdfdsf`;
      });
  },
};
</script>

<style lang="scss" scoped>
@media screen and (max-width: 489px) {
  .p-formgroup-inline {
    .p-field {
      margin-bottom: 1em !important;
    }
  }
}

.layout-content .content-section.implementation > h3 {
  font-weight: 600;
}

textarea {
  resize: none;
}
// body {
//   color: white;
// }
#criteriaDialog {
  width: 100%;
}

#navbar {
  height: 79px;
  background-color: white;
  margin-top: 0 !important;
}
</style>


