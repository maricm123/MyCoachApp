<template>
  <div class="container">
    <div class="columns is-multiline">
      <!-- twit je ritvitovan -->
      <!-- <div v-if="tweet.is_retweet">
        <div
          v-if="currentUser.follows.includes(original_tweet_user.id) || currentUser.id == original_tweet_user.id"
        >
          <div class="column is-12">
            <div class="box">
              <h2 class="subtitle">TweetDetail</h2>
              <p>This tweet is retweeted from {{original_tweet_user.email}} user</p>
              <p>
                <strong>Created at:</strong>
                {{ tweet.created_at }}
              </p>
              <br />
              <br />
              <text>
                <strong>Content:</strong>
                {{ tweet.text }}
              </text>
            </div>
          </div>
      </div>-->
      <!-- ako ga ne prati, ne vidi nista -->
      <!-- <div v-else></div>
      </div>-->

      <div>
        <div class="column is-12">
          <div class="box">
            <h2 class="subtitle">TrainingDetail</h2>

            <p>
              <strong>Created at:</strong>
              {{ training.created_at }}
            </p>
            <br />
            <br />
            <text>
              <!-- <strong>Name:</strong>
              {{ training.name }} -->
            </text>
            <br />
            <br />
            <text>
              <strong>Price:</strong>
              {{ training.price }}
            </text>
            <br />
            <br />
            <text>
              <strong>Sport category:</strong>
              {{ training.sport_category.name }}
            </text>
            <!-- <img :src="tweet.image" alt="Image" />
            {{tweet.image}}-->
          </div>
        </div>
        <div>
          <button @click="subscribe(training.price_id_stripe)" class="button is-info">Subscribe</button>
        </div>
      </div>

      <div class="column is-6">
        <div class="box">
          <h2 class="subtitle">Coached by</h2>

          <!-- <p>
            <strong>Name:</strong>
            {{ training.coach.user.name }}
          </p>-->
          <p>
            <strong>Email:</strong>
            {{ training.coach.user.email }}
          </p>
          <p>
            <strong>Biography:</strong>
            {{ training.coach.biography }}
          </p>
          <p>
            <strong>Sport category:</strong>
            {{ training.coach.sport_category.name }}
          </p>
          <br />
          <!-- <div>
            <button
              v-if="tweet.user.id == currentUser.id"
              class="button is-submit"
              @click="myUserProfile"
            >User profile</button>
            <button
              v-if="tweet.user.id !== currentUser.id"
              class="button is-submit"
              @click="userProfile"
            >User profile</button>
          </div>-->
        </div>
      </div>

      <hr />

      <!-- Only show update and delete buttons if the tweet belongs to the currently logged in user -->
      <!-- <div v-if="tweet.user && currentUser && tweet.user.id === currentUser.id">
        <button class="button is-info" @click="updateTweet">Update</button>
        <button class="button is-danger" @click="deleteTweet">Delete</button>
      </div>-->
      <!-- 
      <div v-if="$store.state.isAuthenticated">
        <button
          class="button"
          :class="{ 'unlike': liked }"
          @click="likeTweet"
        >{{ liked ? 'Unlike' : 'Like' }}</button>
      </div>-->
      <!-- <div v-else>
        You need to
        <a href>login</a> to like this tweet
      </div>-->
      <!-- <div class="liked-by">Liked by: {{liked_by}}</div> -->
      <!-- <div>
        <p>Liked by:</p>
        <ul>
          <li v-for="username in liked_by" v-bind:key="username">{{ username }}</li>
        </ul>
      </div>-->
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "TrainingDetail",
  data() {
    return {
      training: {
        id: null,
        user: {}
      },
      currentUser: null
    };
  },
  async created() {
    await this.$store.dispatch("getCurrentUser").then(currentUser => {
      // Do something with the current user data
      this.currentUser = currentUser;
    });
    await this.getTraining();
    // ako mi ne treba nista od ove fije osim da se storuje u state onda koristim samo ovo:
    //   mounted() {
    //   this.$store.dispatch("getCurrentUser");
    // }
  },
  mounted() {},
  methods: {
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
          // toast({
          //   message: "The tweet was added",
          //   type: "is-success",
          //   dismissible: true,
          //   pauseOnHover: true,
          //   duration: 2000,
          //   position: "bottom-right"
          // });
          this.$router.push("/dashboard/");
        })
        .catch(error => {
          console.log(error);
        });
    },
    // async likeTweet() {
    //   if (
    //     Object.values(this.tweet.liked_by).includes(
    //       this.$store.state.currentUser.username
    //     )
    //   ) {
    //     const tweetID = this.$route.params.id;
    //     await axios
    //       .delete(`/api/tweet/${tweetID}/like/`, {
    //         headers: { Authorization: `Bearer ${this.$store.state.token}` }
    //       })
    //       .then(response => {
    //         this.liked = false;
    //       })
    //       .catch(error => {
    //         console.log(error);
    //       });
    //   } else {
    //     const tweetID = this.$route.params.id;
    //     await axios
    //       .put(
    //         `/api/tweet/${tweetID}/like/`,
    //         {},
    //         {
    //           headers: { Authorization: `Bearer ${this.$store.state.token}` }
    //         }
    //       )
    //       .then(response => {
    //         this.liked = true;
    //       })
    //       .catch(error => {
    //         console.log(error);
    //       });
    //   }
    // },
    // async deleteTweet() {
    //   this.$store.commit("setIsLoading", true);
    //   const tweetID = this.$route.params.id;
    //   await axios
    //     .delete(`/api/tweet/${tweetID}/`, {
    //       headers: { Authorization: `Bearer ${this.$store.state.token}` }
    //     })
    //     .then(response => {
    //       this.$router.push("/dashboard");
    //     })
    //     .catch(error => {
    //       console.log(error);
    //     });
    //   this.$store.commit("setIsLoading", false);
    // },
    async getTraining() {
      this.$store.commit("setIsLoading", true);
      const trainingID = this.$route.params.id;
      await axios
        .get(`/api_coach/program/${trainingID}/`)
        .then(response => {
          this.training = response.data;
          console.log(this.training);
          this.training.user = response.data.user;
          // this.liked_by = response.data.liked_by;
          // if (this.tweet.is_retweet) {
          //   const original_tweet_id = this.tweet.original_tweet;
          //   axios.get(`/api/tweet/${original_tweet_id}`).then(response => {
          //     this.original_tweet_user = response.data.user;
          //   });
          // }
          //   if (
          //     Object.values(response.data.liked_by).includes(
          //       this.$store.state.currentUser.username
          //     )
          //   ) {
          //     // The current user has liked this tweet
          //     this.liked = true;
          //   } else {
          //     this.liked = false;
          //   }
        })
        .catch(error => {
          console.log(error);
        });
    }
    // ova funkcionalnost i delete verovatno ne treba.
    // async updateTweet() {
    //   const tweetID = this.$route.params.id;
    //   // Navigate to the tweet update page
    //   this.$router.push(`/dashboard/tweets/${tweetID}/update/`);
    // },
    // async userProfile() {
    //   // Navigate to the user profile page
    //   this.$router.push(`/dashboard/user-profile/${this.tweet.user.id}`);
    // },
    // async myUserProfile() {
    //   // Navigate to the user profile page
    //   this.$router.push("/dashboard/my-user-profile/");
    // }
  }
};
</script>
<style lang="css" scoped>
.button {
  background-color: rgb(0, 0, 0);
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.unlike {
  background-color: #ffcc00;
  color: rgb(187, 35, 35);
}

.liked-by {
  margin: auto;
}
</style>