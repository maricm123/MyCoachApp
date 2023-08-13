<template>
  <div>
    <h1>Account Confirmation</h1>
    <p v-if="loading">Confirming account...</p>
    <p v-else-if="success">Account confirmed successfully!</p>
    <p v-else>Error confirming account. Please try again later.</p>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      loading: true,
      success: false
    };
  },
  mounted() {
    // Get the confirmation token from the URL
    const token = this.$route.params.token;
    console.log(token, "TOKENN");

    // Call the API to confirm the account using the token
    // Replace 'confirm_account_url' with your Django API endpoint for account confirmation
    axios
      .post("/api/confirmation/", { token })
      .then(response => {
        console.log(response);
        if (response.data.success) {
          this.success = true;
        } else {
          this.success = false;
        }
        this.loading = false;
      })
      .catch(error => {
        console.error(error);
        this.loading = false;
      });
  }
};
</script>
