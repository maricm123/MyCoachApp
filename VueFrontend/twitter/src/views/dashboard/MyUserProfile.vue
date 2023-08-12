<template>
  <div class="container">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">User Profile - {{email}}</h1>
        <button class="button" @click="editUser">Edit profile</button>
        <button @click="logout()" class="button is-danger">Log out</button>
        <button class="button is-light">
          <router-link to="/dashboard/add-tweet">Add your tweet</router-link>
        </button>
      </div>

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
    </div>
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
        <div class="column" v-if="this.privacy == 'PRIVATE'">
          <h2 class="title is-4">Follow Request:</h2>
          <ul class="list is-hoverable">
            <div v-for="followRequests in followRequest" :key="followRequests.id">
              <li class="list-item">{{ followRequests.requester }}</li>
              <button class="button is-info" @click="acceptFollow(followRequests.id)">Accept</button>
              <button class="button is-danger" @click="rejectFollow(followRequests.id)">Reject</button>
            </div>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
export default {
  name: "MyUserProfile",
  data() {
    return {
      tweets: [],
      currentUser: null,
      email: null,
      followers: [],
      followingList: [],
      followRequest: []
    };
  },
  created() {
    this.$store.dispatch("getCurrentUser").then(currentUser => {
      // Do something with the current user data
      this.currentUser = currentUser;
      this.email = currentUser.email;
      this.privacy = currentUser.account_status;
    });
    this.getFollowers();
  },
  methods: {
    async logout() {
      const refresh = localStorage.getItem("refresh");
      await axios
        .post(
          "/api/logout/",
          { refresh },
          {
            headers: { Authorization: `Bearer ${this.$store.state.access}` }
          }
        )
        .then(response => {
          console.log("Logged out");
        })
        .catch(error => {
          console.log(JSON.stringify(error));
        });
      this.$store.commit("removeAccess");
      axios.defaults.headers.common["Authorization"] = "";
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      localStorage.removeItem("role");

      this.$router.push("/login");
    },
    async getUserTweets() {
      await axios
        .get("/api/tweets-by-me/", {
          headers: { Authorization: `Bearer ${this.$store.state.access}` }
        })
        .then(response => {
          this.tweets = response.data;
        });
    },
    async editUser() {
      // Navigate to the tweet update page
      this.$router.push(
        `/dashboard/my-user-profile/edit/${this.currentUser.id}/`
      );
    },
    async getFollowers() {
      await axios
        .get("/api/following-list/", {
          headers: { Authorization: `Bearer ${this.$store.state.access}` }
        })
        .then(response => {
          this.followingList = response.data;
        });
      await axios
        .get("/api/followers-list/", {
          headers: { Authorization: `Bearer ${this.$store.state.access}` }
        })
        .then(response => {
          this.followers = response.data;
        });
      await axios
        .get("/api/follow-request-list/", {
          headers: { Authorization: `Bearer ${this.$store.state.access}` }
        })
        .then(response => {
          this.followRequest = response.data;
        });
    },
    async acceptFollow(follow_request_id) {
      console.log(follow_request_id);
      console.log("accept");
      await axios
        .post(
          `/api/follow-request-action/1/${follow_request_id}/`,
          {},
          {
            headers: { Authorization: `Bearer ${this.$store.state.access}` }
          }
        )
        .then(response => {
          console.log(response.data);
        });
    },
    async rejectFollow(follow_request_id) {
      console.log("reject");
      console.log(follow_request_id);
      await axios
        .post(
          `/api/follow-request-action/2/${follow_request_id}/`,
          {},
          {
            headers: { Authorization: `Bearer ${this.$store.state.access}` }
          }
        )
        .then(response => {
          console.log(response.data);
        });
    }
  },

  mounted() {
    this.getUserTweets();
  }
};
</script>