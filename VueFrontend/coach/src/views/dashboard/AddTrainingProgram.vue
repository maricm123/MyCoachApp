<template>
  <div class="container">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">Add training program</h1>
      </div>

      <div class="column is-12">
        <form @submit.prevent="submitForm">
          <div class="field">
            <label>Name</label>
            <div class="control">
              <input type="text" class="input" v-model="name" />
            </div>
          </div>

          <div class="field">
            <label>Price</label>
            <div class="control">
              <input type="text" class="input" v-model="price" />
            </div>
          </div>

          <div class="field">
            <label for="pdf">PDF File</label>
            <div class="control">
              <input type="file" id="pdf" accept=".pdf" @change="handleFileUpload" />
            </div>
          </div>

          <div class="field">
            <label>Text</label>
            <div class="control">
              <input type="text" class="input" v-model="text" />
            </div>
          </div>

          <div class="field">
            <label>Coach share percentage</label>
            <div class="control">
              <input type="text" class="input" v-model="coach_share_percentage" />
            </div>
          </div>

          <!-- <label for="visibility">Sport category:</label>
          <select id="visibility" v-model="sport_category.name">
            <div v-for="sport_category in sport_category" v-bind:key="sport_category.id">
              <option>{{sport_category}}</option>
            </div>
          </select>-->

          <div class="field">
            <label for="visibility">Sport category:</label>
            <div class="control">
              <select id="visibility" v-model="sport_categories">
                <option
                  value="sport_category"
                  v-for="category in sport_categories"
                  :key="category.id"
                >{{ category.name }}</option>
              </select>
            </div>
          </div>

          <div class="field">
            <div class="control">
              <button class="button is-success">Submit</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { toast } from "bulma-toast";
export default {
  name: "AddTrainingProgram",
  data() {
    return {
      name: "",
      price: "",
      text: "",
      pdf: "",
      coach_share_percentage: "",
      sport_categories: {
        id: "",
        name: ""
      },
      currentUser: {},
    };
  },
  mounted() {
    this.getSportCategories();
  },
  created() {
    this.$store.dispatch("getCurrentUser").then(currentUser => {
      // Do something with the current user data
      this.currentUser = currentUser;
      this.email = currentUser.email;
      console.log(this.currentUser.id)
    });
  },
  methods: {
    async submitForm() {
      this.$store.commit("setIsLoading", true);
      const program = {
        name: this.name,
        price: this.price,
        text: this.text,
        pdf: this.pdf,
        coach_share_percentage: this.coach_share_percentage,
        coach: this.currentUser.id,
        sport_category: 1
      };
      console.log(program)
      await axios
        .post("/api_coach/create-program/", program, {
          headers: { Authorization: `Bearer ${this.$store.state.access}` }
        })
        .then(response => {
          toast({
            message: "The training program was added",
            type: "is-success",
            dismissible: true,
            pauseOnHover: true,
            duration: 2000,
            position: "bottom-right"
          });
          this.$router.push("/dashboard/");
        })
        .catch(error => {
          console.log(error);
        });
      this.$store.commit("setIsLoading", false);
    },
    async getSportCategories() {
      this.$store.commit("setIsLoading", true);
      axios
        .get("/api_coach/sport-categories/", {
          headers: { Authorization: `Bearer ${this.$store.state.access}` }
        })
        .then(response => {
          this.sport_categories = response.data;
        })
        .catch(error => {
          console.log(error);
        });
      this.$store.commit("setIsLoading", false);
    }
  }
};
</script>