<template>
  <div class="container">
    <div class="columns is-multiline" v-if="user.user_type == 'business'">
      <h1>Business type</h1>
      <div class="column is-12">
        <h1 class="title">Edit {{ user.email }}</h1>
      </div>

      <div class="column is-12">
        <form @submit.prevent="submitForm">
          <div class="field">
            <label>Username</label>
            <div class="control">
              <input type="text" class="input" v-model="user.username" />
            </div>
          </div>

          <div class="field">
            <label>Email</label>
            <div class="control">
              <input type="email" class="input" v-model="user.email" />
            </div>
          </div>

          <div class="field">
            <label>Website</label>
            <div class="control">
              <input type="text" class="input" v-model="user.website" />
            </div>
          </div>

          <div class="field">
            <label>Company name</label>
            <div class="control">
              <input type="text" class="input" v-model="user.company_name" />
            </div>
          </div>

          <label for="visibility">Profile Visibility:</label>
          <select id="visibility" v-model="user.account_status">
            <option value="OPEN">Open</option>
            <option value="PRIVATE">Private</option>
          </select>

          <div class="field">
            <div class="control">
              <button class="button is-success">Update</button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <!-- DEFAULT USER EDIT -->

    <div v-else>
      <div class="column is-12">
        <h1>Default type</h1>
        <h1 class="title">Edit {{ user.email }}</h1>
      </div>

      <div class="column is-12">
        <form @submit.prevent="submitForm">
          <div class="field">
            <label>Username</label>
            <div class="control">
              <input type="text" class="input" v-model="user.username" />
            </div>
          </div>

          <div class="field">
            <label>Email</label>
            <div class="control">
              <input type="email" class="input" v-model="user.email" />
            </div>
          </div>

          <div class="field">
            <label>First name</label>
            <div class="control">
              <input type="text" class="input" v-model="user.first_name" />
            </div>
          </div>

          <div class="field">
            <label>Last name</label>
            <div class="control">
              <input type="text" class="input" v-model="user.last_name" />
            </div>
          </div>

          <div class="field">
            <label>Agee</label>
            <div class="control">
              <input type="text" class="input" v-model="user.age" />
            </div>
          </div>

          <div class="field">
            <label>Address</label>
            <div class="control">
              <input type="text" class="input" v-model="user.address" />
            </div>
          </div>

          <label for="visibility">Profile Visibility:</label>
          <select id="visibility" v-model="user.account_status">
            <option value="OPEN">Open</option>
            <option value="PRIVATE">Private</option>
          </select>

          <div class="field">
            <div class="control">
              <button class="button is-success">Update</button>
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
  name: "EditUserProfile",
  data() {
    return {
      user: {}
    };
  },
  mounted() {
    this.getUser();
  },
  methods: {
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
    async submitForm() {
      this.$store.commit("setIsLoading", true);
      const userID = this.$route.params.id;
      axios
        .patch(`/api/my-profile/${userID}/`, this.user, {
          headers: { Authorization: `Bearer ${this.$store.state.token}` }
        })
        .then(response => {
          toast({
            message: "The user was updated",
            type: "is-success",
            dismissible: true,
            pauseOnHover: true,
            duration: 2000,
            position: "bottom-right"
          });
          this.$router.push(`/dashboard/my-user-profile/`);
        })
        .catch(error => {
          console.log(error);
        });
      this.$store.commit("setIsLoading", false);
    }
  }
};
</script>