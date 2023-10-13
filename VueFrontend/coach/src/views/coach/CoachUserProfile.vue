<template>
    <div class="container">
        <div class="columns is-multiline">
          <div class="column is-12">
            <h1 class="title">User Profile - {{email}}</h1>
            <button class="button" @click="editUser">Edit profile</button>
            <button class="button is-light">
              <router-link to="/dashboard/coach-user-profile/add-training-program">Add training program</router-link>
            </button>
            <button @click="logout()" class="button is-danger">Log out</button>
          </div>
      
          <!-- ovde u if dodati jos ako currentUser prati usera kojem smo na profilu onda moze da vidi ovo -->
          <div>
            <div class="card" v-for="program in programs" v-bind:key="program.id">
              <div class="card-content">
                  
                  <div class="media-content">
                    <p class="title is-4">{{program.name}}</p>
                    <p class="subtitle is-6">{{program.sport_category.name}}</p>
                  </div>
    
                <div class="content">
                  <br />
                  <time>{{program.created_at}}</time>
                </div>
              </div>
              <button class="button is-white">
                <router-link :to="{ name: 'TrainingDetail', params: { id: program.id }}">Details</router-link>
              </button>
            </div>
          </div>
        </div>
      </div>
      {{parsedDate}}
</template>
  
<script>
import axios from "axios";
import { toast } from "bulma-toast";

export default {
  name: "UserProfile",
  data() {
    return {
      programs: [],
      currentUser: null,
      user: {},
      email: null,
      parsedDate: null,
    };
  },
  async mounted() {
    await this.$store.dispatch("getCurrentUser").then(currentUser => {
        
      // Do something with the current user data
      this.currentUser = currentUser;
      this.email = currentUser.email;
    });
  },
  
  async created() {
    await this.getUserTrainings();
    
  },
  methods: {
    async logout() {
      const refresh = localStorage.getItem("refresh");
      await axios
        .post(
          "/api_coach/logout/",
          { refresh },
          {
            headers: { Authorization: `Bearer ${this.$store.state.access}` }
          }
        )
        .then(response => {
          console.log("Logged out");
        })
        .catch(error => {
          console.log("ERROR");
          console.log(JSON.stringify(error));
        });
      this.$store.commit("removeAccess");
      axios.defaults.headers.common["Authorization"] = "";
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      localStorage.removeItem("role");

      this.$router.push("/login");
    },
    async getUserTrainings() {
      await axios
        .get("/api_coach/programs-by-me/", {
          headers: { Authorization: `Bearer ${this.$store.state.access}` }
        })
        .then(response => {
          this.programs = response.data;
          console.log(this.programs)
        })
        .catch(error => {
          console.log(error);
        });
    },
    
  }
};
  </script>
  
  <style scoped>
  .card {
    margin-bottom: 5%;
  }
  
  </style>