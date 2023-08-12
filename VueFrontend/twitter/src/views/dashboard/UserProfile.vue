<template>
  <div class="container">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">User Profile - {{user.email}}</h1>
        <!-- ovde ide v-if ako currentUser prati ovog usera onda ide button za unffollow -->
        <button
          class="button is-black"
          @click="followUser"
          :class="{ 'requested': followStatus === 'requested', 'following': followStatus === 'following' }"
        >
          <span v-if="followStatus === 'not-following'">Follow User</span>
          <span v-else-if="followStatus === 'requested'">Requested</span>
          <span v-else-if="followStatus === 'following'">Following</span>
        </button>
        <!-- <button class="button is-black" style="font-color: white">Unfollow user</button> -->
      </div>
      <!-- ovde u if dodati jos ako currentUser prati usera kojem smo na profilu onda moze da vidi ovo -->
      <div v-if="user.account_status == 'OPEN' || followStatus == 'following'">
        <div class="card" v-for="tweet in tweets" v-bind:key="tweet.id">
          <div class="card-content">
            <div class="media">
              <div class="media-left">
                <figure class="image is-48x48">
                  <img src="https://bulma.io/images/placeholders/96x96.png" alt="Placeholder image" />
                </figure>
              </div>
              <div class="media-content">
                <p class="title is-4">{{tweet.user.username}}</p>
                <p class="subtitle is-6">{{tweet.user.email}}</p>
              </div>
            </div>

            <div class="content">
              {{tweet.text}}
              <br />
              <time>{{tweet.created_at}}</time>
            </div>
          </div>
          <button class="button is-black" style="font-color: white">
            <router-link :to="{ name: 'TweetDetail', params: { id: tweet.id }}">Details</router-link>
          </button>
        </div>
        <br />
        <div class="container">
          <div class="columns">
            <div class="column">
              <h2 class="title is-4">Followers:</h2>
              <ul class="list is-hoverable">
                <li
                  v-for="follower in followers"
                  :key="follower.id"
                  class="list-item"
                >{{ follower.email }}</li>
              </ul>
            </div>
            <div class="column">
              <h2 class="title is-4">Following:</h2>
              <ul class="list is-hoverable">
                <li
                  v-for="following in followingList"
                  :key="following.id"
                  class="list-item"
                >{{ following.email }}</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { toast } from "bulma-toast";

export default {
  name: "UserProfile",
  data() {
    return {
      currentUser: null,
      tweets: [],
      user: {},
      followers: [],
      followingList: [],
      followRequest: [],
      followStatus: "not-following", // or 'requested' or 'following',
      userID: null,
      follows: [],
      email: "",
      privacy: ""
    };
  },
  async mounted() {
    await this.$store.dispatch("getCurrentUser").then(currentUser => {
      // Do something with the current user data
      this.currentUser = currentUser;
    });

    this.userID = this.$route.params.id;
  },

  async created() {
    await this.getUser();
    await this.getFollowers();
    await this.checkFollow();
  },
  methods: {
    async checkFollow() {
      const userID = this.$route.params.id;
      const userIdNumber = parseInt(userID);
      await axios
        .get("/api/do-i-request-list/", {
          headers: { Authorization: `Bearer ${this.$store.state.token}` }
        })
        .then(response => {
          this.followRequest = response.data;
        });
      const toFollowArray = [];
      for (const obj of this.followRequest) {
        toFollowArray.push(obj.to_follow);
      }

      if (this.currentUser.follows.includes(userIdNumber)) {
        console.log("CURRENT USER PRATI OVOG USERA");
        this.followStatus = "following";
        this.getUserTweets();
      } else if (toFollowArray.includes(this.user.email)) {
        console.log("CURRENT USER REQUEST TO FOLLOW THISS USER");

        this.followStatus = "requested";
        // ovde proveravamo da li mu je poslat zaahtev za pracenje
      } else {
        console.log("current user NEEEEE prati ovog usera");
        this.followStatus = "not-following";
        if (this.user.account_status == "OPEN") {
          this.getUserTweets();
        }
      }
    },
    async getUserTweets() {
      const userID = this.$route.params.id;
      await axios
        .get(`/api/tweets-by-user/${userID}`, {
          headers: { Authorization: `Bearer ${this.$store.state.token}` }
        })
        .then(response => {
          this.tweets = response.data;
        });
    },
    async getUser() {
      this.$store.commit("setIsLoading", true);
      const userID = this.$route.params.id;
      axios
        .get(`/api/my-profile/${userID}/`)
        .then(response => {
          this.user = response.data;
        })
        .catch(error => {
          console.log(error);
        });
      this.$store.commit("setIsLoading", false);
    },
    async followUser() {
      this.$store.commit("setIsLoading", true);
      const tweet = {
        to_follow_id: this.userID
      };
      await axios
        .post(`/api/follow-user/${this.userID}/`, tweet, {
          headers: { Authorization: `Bearer ${this.$store.state.token}` }
        })
        .then(response => {
          if (response.data.detail == "requested") {
            this.followStatus = "requested";
            console.log(response.data.detail);
            console.log("PRIVATE PROFIL");
            toast({
              message: "You requested to follow this user",
              type: "is-success",
              dismissible: true,
              pauseOnHover: true,
              duration: 2000,
              position: "bottom-right"
            });
          } else {
            this.followStatus = "following";

            console.log("OPENED PROFILE");
            toast({
              message: "You now following this user",
              type: "is-success",
              dismissible: true,
              pauseOnHover: true,
              duration: 2000,
              position: "bottom-right"
            });
          }
          this.$router.push(`/dashboard/user-profile/${this.userID}/`);
        })
        .catch(error => {
          console.log(error);
        });
      this.$store.commit("setIsLoading", false);
    },
    //
    //
    //
    //
    //
    async getFollowers() {
      const userID = this.$route.params.id;
      await axios
        .get(`/api/following-list/${userID}/`, {
          headers: { Authorization: `Bearer ${this.$store.state.token}` }
        })
        .then(response => {
          this.followingList = response.data;
        });
      await axios
        .get(`/api/followers-list/${userID}/`, {
          headers: { Authorization: `Bearer ${this.$store.state.token}` }
        })
        .then(response => {
          this.followers = response.data;
        });
    }
  }
};
</script>