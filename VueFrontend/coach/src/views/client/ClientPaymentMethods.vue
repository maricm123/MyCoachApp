<template>
    <div v-for="payment_method in payment_methods" v-bind="payment_method">
        {{ payment_method }}
        <button>Set default card</button>
        <button @click="deletePaymentMethod(payment_method.id)">delete</button>
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
        // async deletePaymentMethod() {
        //     await axios
        //         .delete("/api_coach/delete-payment_method/", {
        //             headers: { Authorization: `Bearer ${this.$store.state.access}` }
        //         })
        //         .then(response => {
        //             console.log(response.data)
        //             this.payment_methods = response.data;
        //         });
        // },
        async deletePaymentMethod(payment_method_id) {
            this.$store.commit("setIsLoading", true);
            // const payment_method_id = this.$route.params.id;
            await axios
                .delete(`/api_coach/delete-payment-method/${payment_method_id}/`, {
                headers: { Authorization: `Bearer ${this.$store.state.access}` }
                })
                .then(response => {
                    console.log(response.data)
                    this.$router.push("/dashboard/my-user-profile/get-payment-methods");
                })
                .catch(error => {
                console.log(error);
                });
            this.$store.commit("setIsLoading", false);
            },
    }

}
</script>

<style>

</style>