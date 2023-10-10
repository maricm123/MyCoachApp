<template>
    <div v-for="payment_method in payment_methods" v-bind="payment_method" class="card">
        <header class="card-header">
          <p  class="card-header-title">
            Credit card <span class="default" v-if="payment_method.is_default == true"> Default card</span>
          </p>
          <button class="card-header-icon" aria-label="more options">
            <span class="icon">
              <i class="fas fa-angle-down" aria-hidden="true"></i>
            </span>
          </button>
        </header>
        <div class="card-content">
          <div class="content">
            <p class="text">Number:</p>
            {{ payment_method.number }}            
        </div>
        <p class="text">Expiry date:</p>
        {{ payment_method.exp_month }} / {{ payment_method.exp_year }}
        </div>
        <footer class="card-footer">
          <a @click="setPaymentMethodDefault(payment_method.id)" class="card-footer-item">Set default card</a>
          <a @click="deletePaymentMethod(payment_method.id)" class="card-footer-item">Delete</a>
        </footer>
      </div>
  
</template>

<script>
import axios from 'axios';
export default {
    name: "ClientPaymentMethods",
    data() {
        return {
            payment_methods: []

        }
    },
    created() {
        this.getUserTrainings();
    },
    methods: {
        async getUserTrainings() {
            await axios
                .get("/api_coach/get-payment-methods/", {
                headers: { Authorization: `Bearer ${this.$store.state.access}` }
                })
                .then(response => {
                    console.log(response.data)
                    this.payment_methods = response.data;
                });
            },
        async deletePaymentMethod(payment_method_id) {
            this.$store.commit("setIsLoading", true);
            // const payment_method_id = this.$route.params.id;
            await axios
                .delete(`/api_coach/delete-payment-method/${payment_method_id}/`, {
                headers: { Authorization: `Bearer ${this.$store.state.access}` }
                })
                .then(response => {
                    console.log(response.data)
                    this.$router.push("/dashboard/client-user-profile/get-payment-methods");
                })
                .catch(error => {
                console.log(error);
                });
            this.$store.commit("setIsLoading", false);
            },
        async setPaymentMethodDefault(payment_method_id) {
            this.$store.commit("setIsLoading", true);
            // const payment_method_id = this.$route.params.id;
            await axios
            .post(
                "/api_coach/set-payment-method-default/",
                {payment_method_id},
                {
                    headers: { Authorization: `Bearer ${this.$store.state.access}` }
                }
                )
                .then(response => {
                    console.log(response.data)
                    this.$router.push("/dashboard/client-user-profile/get-payment-methods");
                })
                .catch(error => {
                console.log(error);
                });
            this.$store.commit("setIsLoading", false);
            },
    }

}
</script>

<style scoped>
.card {
    margin-bottom: 5%;
}
.default {
    font-weight: bold;
    margin-left: 79%;
}
</style>