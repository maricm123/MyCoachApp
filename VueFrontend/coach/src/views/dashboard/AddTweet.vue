<template>
  <div class="container">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">Add tweet</h1>
      </div>

      <div class="column is-12">
        <form @submit.prevent="submitForm">
          <div class="field">
            <label>Text</label>
            <div class="control">
              <input type="text" class="input" v-model="text" />
            </div>
          </div>

          <div class="field">
            <label>Image</label>
            <div class="control">
              <input type="file" accept="image/*" @change="handleImageUpload" />
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
  name: "AddTweet",
  data() {
    return {
      text: "",
      image: ""
    };
  },
  methods: {
    async submitForm() {
      this.$store.commit("setIsLoading", true);
      const tweet = {
        text: this.text,
        image: null
      };
      await axios
        .post("/api/tweet-create/", tweet, {
          headers: { Authorization: `Bearer ${this.$store.state.token}` }
        })
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
      this.$store.commit("setIsLoading", false);
    }
  }
};
</script>