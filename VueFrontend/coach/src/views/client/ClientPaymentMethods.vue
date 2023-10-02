<template>
    <div>
        {{ payment_methods }}
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
            }
    }

}
</script>

<style>

</style>