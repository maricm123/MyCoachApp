<template>
  <div class="container">
    <div>
        <div class="column is-12">
          <div class="box">
            <h2 class="subtitle">TrainingDetail</h2>

            <p>
              <strong>Created at:</strong>
              {{ training.created_at }}
            </p>
            <text>
                <strong>Name:</strong>
                {{ training.name }}
              </text>
          </div>
          
        </div>
        <div class="column is-6">
            <div class="box">
                <p>
                    <strong>Email:</strong>
                    {{ training.coach.user.email }}
                </p>
                <button
                    class="button is-submit"
                    @click="myUserProfile"
                >
                    User profile
                </button>
            </div>
            <div>
      
          </div>
        </div>
        <div>
            <button @click="subscribe(training.price_id_stripe)" class="button is-info">Subscribe</button>
          </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';
import { toast } from "bulma-toast";

export default {
    name: "TrainingDetail2",
    data() {
        return {
            training: [],
            currentUser: {}
        }
    },
    async created() {
        await this.$store.dispatch("getCurrentUser").then(currentUser => {
            // Do something with the current user data
            this.currentUser = currentUser;
        });
        await this.getTraining();
    },
    mounted() {},
    methods: {
        async getTraining() {
            this.$store.commit("setIsLoading", true);
            const trainingID = this.$route.params.id;
            await axios
                .get(`/api_coach/program/${trainingID}/`)
                .then(response => {
                    this.training = response.data;
                    console.log(this.training);
                    this.training.user = response.data.user;
                })
                    .catch(error => {
                    console.log(error);
                });
        },
        async subscribe(price_id_stripe) {
            const program = {
                price_id_stripe: price_id_stripe
            };
            await axios
                .post("/api_coach/create-subscription/", program, {
                headers: { Authorization: `Bearer ${this.$store.state.access}` }
                })
                .then(response => {
                    console.log(response.data);
                    toast({
                      message: "You are subscribed to this program, check your email",
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
            },
    },
}
</script>

<style>

</style>