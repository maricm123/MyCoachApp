<template>
  <div class="container">
    <div class="columns">
      <div class="column is-4 is-offset-4">
        <h1 class="title">Log in</h1>

        <form @submit.prevent="submitForm">
          <div class="field">
            <label>Email</label>
            <div class="control">
              <input type="email" name="email" class="input" v-model="email" />
            </div>
          </div>

          <div class="field">
            <label>Password</label>
            <div class="control">
              <input type="password" name="password" class="input" v-model="password" />
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
        <br />
        <!-- <div class="control">
          <button class="button is-dark" @click="forgotPassword()">Forgot Password?</button>
        </div>-->
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
      password: "",
      errors: []
    };
  },
  methods: {
    async submitForm() {
      this.$store.commit("setIsLoading", true);

      axios.defaults.headers.common["Authorization"] = "";
      localStorage.removeItem("access");

      const formData = {
        email: this.email,
        password: this.password
      };
      await axios
        .post("/api_coach/user/login/", formData)
        .then(response => {
          console.log(response);
          const access = response.data.access;
          const refresh = response.data.refresh;
          const role = response.data.role;

          this.$store.commit("setAccess", access);
          this.$store.commit("setRefresh", refresh);
          this.$store.commit("setRole", role);

          axios.defaults.headers.common["Authorization"] = "Token " + access;

          localStorage.setItem("access", access);
          localStorage.setItem("refresh", refresh);
          localStorage.setItem("role", role);
          this.$router.push("/dashboard/subscribe");
        })
        .catch(error => {
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
    // forgotPassword() {
    //   this.$router.push("/forgot-password");
    // }
  }
};
</script>