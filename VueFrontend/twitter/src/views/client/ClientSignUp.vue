<template>
  <div class="container">
    <div class="columns">
      <div class="column is-4 is-offset-4">
        <h1 class="title">Client - sign up</h1>

        <form @submit.prevent="submitForm">
          <div class="field">
            <label>Name</label>
            <div class="control">
              <input type="text" name="name" class="input" v-model="name" />
            </div>
          </div>
          <div class="field">
            <label>Password</label>
            <div class="control">
              <input type="password" name="password" class="input" v-model="password" />
            </div>
          </div>

          <div class="field">
            <label>Repeat password</label>
            <div class="control">
              <input type="password" name="password2" class="input" v-model="password2" />
            </div>
          </div>

          <div class="field">
            <label>Email</label>
            <div class="control">
              <input type="text" name="email" class="input" v-model="email" />
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
import { toast } from "bulma-toast";
export default {
  name: "ClientSignUp",
  data() {
    return {
      name: "",
      password: "",
      email: "",
      password2: "",
      role: "client",
      errors: []
    };
  },
  methods: {
    async submitForm() {
      this.errors = [];

      if (this.name === "") {
        this.errors.push("The name is missing");
      }
      if (this.password === "") {
        this.errors.push("The password is too short");
      }
      if (this.password !== this.password2) {
        this.errors.push("The password are not matching");
      }
      if (!this.errors.length) {
        this.$store.commit("setIsLoading", true);
        const user = {
          user: {
            email: this.email,
            name: this.name,
            password: this.password,
            role: this.role
          }
        };
        await axios
          .post("http://127.0.0.1:8000/api_coach/client/register/", user)
          .then(response => {
            toast({
              message: "Account was created, please log in",
              type: "is-success",
              dismissible: true,
              pauseOnHover: true,
              duration: 2000,
              position: "bottom-right"
            });
            this.$router.push("/login");
          })
          .catch(error => {
            if (error.response) {
              for (const property in error.response.data) {
                this.errors.push(
                  `${property}: ${error.response.data[property]}`
                );
              }
            } else if (error.message) {
              this.errors.push("Something went wrong. Please try again!");
            }
          });

        this.$store.commit("setIsLoading", false);
      }
    }
  }
};
</script>