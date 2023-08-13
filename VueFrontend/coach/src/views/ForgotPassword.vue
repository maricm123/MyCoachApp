<template>
  <div class="container">
    <div class="columns">
      <div class="column is-4 is-offset-4">
        <h1 class="title">Forgot password?</h1>

        <form @submit.prevent="submitForm">
          <div class="field">
            <label>Email</label>
            <div class="control">
              <input type="email" name="email" class="input" v-model="email" />
            </div>
          </div>
          <div class="notification is-danger" v-if="errors.length">
            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
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

export default {
  name: "Login",
  data() {
    return {
      email: "",
      errors: []
    };
  },
  methods: {
    async submitForm() {
      this.$store.commit("setIsLoading", true);

      //   axios.defaults.headers.common["Authorization"] = "";
      //   localStorage.removeItem("token");

      const formData = {
        email: this.email
      };
      await axios
        .post("/api/forgot-password/", formData)
        .then(response => {
          console.log(response);
          alert("Check confirmation link in your email.");
          //   const token = response.data.token;
          //   const refresh = response.data.refresh;
          //   const role = response.data.user_type;

          //   this.$store.commit("setToken", token);
          //   this.$store.commit("setRefresh", refresh);
          //   this.$store.commit("setRole", role);

          //   axios.defaults.headers.common["Authorization"] = "Token " + token;

          //   localStorage.setItem("token", token);
          //   localStorage.setItem("refresh", refresh);
          //   localStorage.setItem("role", role);
          this.$router.push("/login");
        })
        .catch(error => {
          console.log(error);
          if (error.response) {
            for (const message in error.response.data) {
              this.errors.push(`${message}: ${error.response.data[message]}`);
            }
          } else if (error.message) {
            this.errors.push("Something went wrong. Please try again!");
          }
        });

      this.$store.commit("setIsLoading", false);
    }
  }
};
</script>