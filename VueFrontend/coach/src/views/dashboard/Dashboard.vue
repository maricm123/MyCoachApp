<template>
  <div class="container">
    <div class="columns is-multiline">
      <div v-if="$store.state.isAuthenticated" class="column is full">
        <!-- <button class="button is-gray">
          <router-link to="/dashboard/add-tweet">Add your training plan</router-link>
        </button>-->
        <div class="column is-full">
          <h1 class="title">Training plans</h1>
        </div>
        <div class="program" v-for="program in programs" v-bind:key="program.id">
          <div class="card">
            <div class="card-content">
              <div class="content">{{program.name}}</div>
            </div>
            <footer class="card-footer">
              <router-link
                class="card-footer-item"
                :to="{ name: 'TrainingDetail', params: { id: program.id }}"
              >Subscribe</router-link>
            </footer>
            <nav class="level is-mobile">
              <div class="level-item has-text-centered">
                <div>
                  <p class="heading">Coach</p>
                  <p class="title">{{program.coach.user.name}}</p>
                </div>
              </div>
              <div class="level-item has-text-centered">
                <div>
                  <p class="heading">Price</p>
                  <p class="title">{{program.price}}</p>
                </div>
              </div>
              <div class="level-item has-text-centered">
                <div>
                  <p class="heading">Followers</p>
                  <p class="title">456K</p>
                </div>
              </div>
              <div class="level-item has-text-centered">
                <div>
                  <p class="heading">Likes</p>
                  <p class="title">789</p>
                </div>
              </div>
            </nav>
          </div>
        </div>
      </div>
      <div v-else>NotAuth</div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "Dashboard",
  data() {
    return {
      programs: []
    };
  },
  mounted() {
    this.getPrograms();
  },
  methods: {
    async getPrograms() {
      this.$store.commit("setIsLoading", true);
      axios
        .get("/api_coach/program/", {
          headers: { Authorization: `Bearer ${this.$store.state.access}` }
        })
        .then(response => {
          this.programs = response.data;
          console.log(this.programs);
        })
        .catch(error => {
          console.log(error);
        });
      this.$store.commit("setIsLoading", false);
    }
  }
};
</script>
<style scoped>
.program {
  margin: 20px;
}

.level {
  padding: 10px;
}

.card-footer {
  background-color: blue;
  color: white;
}
.card-footer-item {
  color: white;
  font-size: 23px;
}

.content {
  font-size: 23px;
}
</style>