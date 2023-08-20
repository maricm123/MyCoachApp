<template>
  <div>
    <h1>Subscription</h1>
    <div class="subscription">
      <div class="starter-div">
        <h2>Starter plan</h2>
        <img
          class="month-img"
          src="https://img.freepik.com/free-vector/subscriber-concept-illustration_114360-3453.jpg?t=st=1654685116~exp=1654685716~hmac=b67fdd003003bc4f477b5184b2201a36a5a88ebefc2552ee7f4f723a2acef85f&w=740"
        />
        <form @submit.prevent="submitSubscription('price_1NhAE1ATnYPr6yDB8Xg5aCYP')">
          <input type="hidden" name="price_id" value="price_1NhAE1ATnYPr6yDB8Xg5aCYP" />
          <button class="btn-month" type="submit">&#8377;30 / Month</button>
        </form>
      </div>
      <br />
      <div class="premium-div">
        <h2>Premium plan</h2>
        <img
          class="year-img"
          src="https://img.freepik.com/free-vector/subscriber-concept-illustration_114360-2949.jpg?t=st=1654651458~exp=1654652058~hmac=fc1ea117f4198608284f1fea2f5af8f4c50f75692b80c711ad5c93793d0f3ab0&w=740"
        />
        <form @submit.prevent="submitSubscription('price_1NhAE1ATnYPr6yDB8Xg5aCYP')">
          <input type="hidden" name="price_id" value="price_1NhAE1ATnYPr6yDB8Xg5aCYP" />
          <button class="btn-year" type="submit">&#8377;350 /Year</button>
        </form>
      </div>
    </div>
    <br />
  </div>
</template>

<script>
// import { API_URL } from "@/Config/config"; // Adjust the import path based on your project structure
import axios from "axios";

export default {
  name: "Success",
  methods: {
    async submitSubscription(priceId) {
      console.log(priceId);
      await axios
        .post("/api_coach/create-subscription/", priceId, {})
        .then(response => {
          toast({
            message: "The tweet was added",
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
    }
  }
};
</script>

<style scoped>
/* Add your CSS styles here */
</style>