<template>
  <div class="container">
    <div class="columns">
      <div class="column is-4 is-offset-4">
        <h1 class="title">Reset password</h1>
        <form @submit="resetPassword">
          <div class="field">
            <label>New password</label>
            <div class="control">
              <input
                type="password"
                v-model="newPassword"
                class="input"
                placeholder="New Password"
                required
              />
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
export default {
  data() {
    return {
      newPassword: ""
    };
  },
  async created() {
    // Get the uid and token from the URL parameters
    // this.uid = this.$route.params.uid;
    this.uid = await this.$route.params.uid;
    this.token = await this.$route.params.token;
    console.log(this.token);
  },
  methods: {
    resetPassword() {
      const payload = {
        uid: this.uid,
        token: this.token,
        new_password: this.newPassword
      };

      axios
        .post("/api/reset-password/", payload)
        .then(response => {
          console.log(response);
          // Handle success response (e.g., show a success message)
        })
        .catch(error => {
          console.log(error);
          // Handle error response (e.g., show an error message)
        });
    }
  }
};
</script>
