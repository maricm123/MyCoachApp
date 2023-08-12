<template>
  <div>
    <Navbar />
    <section class="section">
      <router-view />
    </section>
  </div>
</template>

<script>
import axios from "axios";
import Navbar from "@/components/layout/Navbar";
export default {
  name: "App",
  components: {
    Navbar
  },
  beforeCreate() {
    this.$store.commit("initializeStore");

    // token je proveren svaki put kada zelimo da koristimo axios
    if (this.$store.state.access) {
      axios.defaults.headers.common["Authorization"] =
        "Token " + this.$store.state.access;
    } else {
      axios.defaults.headers.common["Authorization"] = "";
    }
  }
};
</script>
<style lang="scss">
@import "../node_modules/bulma";
</style>
