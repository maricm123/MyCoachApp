<template>
  <div class="container">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">User Profile - {{email}}</h1>
        <button class="button" @click="editUser">Edit profile</button>
        <button class="button is-light">
          <router-link to="/dashboard/client-user-profile/create-payment-method">Add your credit card</router-link>
        </button>
        <button class="button is-light">
          <router-link to="/dashboard/client-user-profile/get-payment-methods">Payment cards</router-link>
        </button>
        <button @click="logout()" class="button is-danger">Log out</button>
      </div>
      <br />
      <div class="card" v-for="program in programs" v-bind:key="program.id">
        <div class="card-content">
          <div class="media">
            <div class="media-left">
              <!-- <figure class="image is-48x48">
                <img src="https://bulma.io/images/placeholders/96x96.png" alt="Placeholder image" />
              </figure>-->
              <p class="title is-4">{{program.name}}</p>
            </div>
            <div class="media-content"></div>
          </div>

          <!-- <div class="content">
            {{program.price}}
            <br />
            <time>{{program.created_at}}</time>
          </div>-->
        </div>
        <button class="button" style="font-color: white">
          <router-link :to="{ name: 'TrainingDetail', params: { id: program.id }}">Details</router-link>
        </button>
      </div>
    </div>
    <!-- <div class="container">
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
    </div>-->
    <h1 class="title"> Subscribes </h1>
    
    <div v-for="subscribe in subscribeList" v-bind:key="subscribe.id" class="card">
      <header class="card-header">
        <p class="card-header-title">
          {{subscribe.training_program.name}}
        </p>
        <p class="price">
          {{subscribe.training_program.price}}$ / month
        </p>
        <button class="card-header-icon" aria-label="more options">
          <span class="icon">
            <i class="fas fa-angle-down" aria-hidden="true"></i>
          </span>
        </button>
      </header>
      <div class="card-content">
        <div class="content">
          <p>Status - {{subscribe.status}} </p>
          <p>Registered - {{subscribe.created_at}}</p>
          <time >Next payment - {{subscribe.current_period_end }}</time>
        </div>
      </div>
      <footer class="card-footer">
       
        <a href="#" class="card-footer-item">Check program</a>
        <a href="#" class="card-footer-item">Re-subscribe</a>
        <a href="#" class="card-footer-item">Cancel subscribe</a>
      </footer>
    </div>
    <br/>
    <h1 class="title"> Payments </h1>

    <div v-for="subscribe in subscribeList" v-bind:key="subscribe.id" class="card">
      <header class="card-header">
        <p class="card-header-title">
          {{subscribe.training_program.name}}
        </p>
        <p class="price">
          {{subscribe.training_program.price}}$ / month
        </p>
        <button class="card-header-icon" aria-label="more options">
          <span class="icon">
            <i class="fas fa-angle-down" aria-hidden="true"></i>
          </span>
        </button>
      </header>
      <div class="card-content">
        <div class="content">
          <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Illo soluta nam nobis odit dolo </p>
          <p>Registered - {{subscribe.created_at}}</p>
          <time >Next payment - {{subscribe.current_period_end }}</time>
        </div>
      </div>
    </div>
  </div>
</template> 
<script>
import axios from "axios";
export default {
  name: "ClientUserProfile",
  data() {
    return {
      programs: [],
      currentUser: {},
      email: null,
      subscribeList: [],
      payments: [],
    };
  },
  created() {
    this.$store.dispatch("getCurrentUser").then(currentUser => {
      // Do something with the current user data
      this.currentUser = currentUser;
      this.email = currentUser.email;
    });
    this.getSubscribesAndPayments();
  },
  methods: {
    async logout() {
      const refresh = localStorage.getItem("refresh");
      await axios
        .post(
          "/api_coach/logout/",
          { refresh },
          {
            headers: { Authorization: `Bearer ${this.$store.state.access}` }
          }
        )
        .then(response => {
          console.log("Logged out");
        })
        .catch(error => {
          console.log("ERROR");
          console.log(JSON.stringify(error));
        });
      this.$store.commit("removeAccess");
      axios.defaults.headers.common["Authorization"] = "";
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      localStorage.removeItem("role");

      this.$router.push("/login");
    },
    // async editUser() {
    //   // Navigate to the tweet update page
    //   this.$router.push(
    //     `/dashboard/my-user-profile/edit/${this.currentUser.id}/`
    //   );
    // }
    async getSubscribesAndPayments() {
      await axios
        .get("/api_coach/subscribe-list/", {
          headers: { Authorization: `Bearer ${this.$store.state.access}` }
        })
        .then(response => {
          this.subscribeList = response.data;
        })
        .catch(error => {
          console.log(error);
        });
        
      // await axios
      //   .get("/api_coach/payment-list/", {
      //     headers: { Authorization: `Bearer ${this.$store.state.access}` }
      //   })
      //   .then(response => {
      //     console.log(response.data)
      //     this.payments = response.data;
      //   });
      // await axios
      //   .get("/api/follow-request-list/", {
      //     headers: { Authorization: `Bearer ${this.$store.state.access}` }
      //   })
      //   .then(response => {
      //     this.followRequest = response.data;
      //   });
    },
    // async acceptFollow(follow_request_id) {
    //   console.log(follow_request_id);
    //   console.log("accept");
    //   await axios
    //     .post(
    //       `/api/follow-request-action/1/${follow_request_id}/`,
    //       {},
    //       {
    //         headers: { Authorization: `Bearer ${this.$store.state.access}` }
    //       }
    //     )
    //     .then(response => {
    //       console.log(response.data);
    //     });
    // },
    // async rejectFollow(follow_request_id) {
    //   console.log("reject");
    //   console.log(follow_request_id);
    //   await axios
    //     .post(
    //       `/api/follow-request-action/2/${follow_request_id}/`,
    //       {},
    //       {
    //         headers: { Authorization: `Bearer ${this.$store.state.access}` }
    //       }
    //     )
    //     .then(response => {
    //       console.log(response.data);
    //     });
    // }
  },

  mounted() {
  }
};
</script>
<style scoped>
.card {
  margin-top: 40px;
}

.price {
  font-weight: 700;
  text-align: right;
  padding: 0.75rem 1rem;
}
</style>