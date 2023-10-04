<template>
    <form class="box" id="creditCardForm">
        <div class="field">
          <label class="label">Card Number</label>
          <div class="control">
            <input class="input" type="text" placeholder="Card Number" name="cardNumber" id="cardNumber">
          </div>
        </div>
      
        <div class="field">
          <label class="label">Expiration Date</label>
          <div class="field is-grouped">
            <div class="control">
              <input class="input" type="text" placeholder="MM" name="expMonth" id="expMonth">
            </div>
            <div class="control">
              <input class="input" type="text" placeholder="YYYY" name="expYear" id="expYear">
            </div>
          </div>
        </div>
      
        <div class="field">
          <label class="label">CVC</label>
          <div class="control">
            <input class="input" type="text" placeholder="CVC" name="cvc" id="cvc">
          </div>
        </div>
      
        <button class="button is-primary" type="button" @click="validateCreditCard()">Submit</button>
      </form>
</template>

<script>
import axios from 'axios';

export default {
    name: "CreatePaymentMethod",
    methods: {
        validateCreditCard() {
        const cardNumber = document.getElementById('cardNumber').value;
        const expMonth = document.getElementById('expMonth').value;
        const expYear = document.getElementById('expYear').value;
        const cvc = document.getElementById('cvc').value;

        // Perform validation checks here (e.g., card number format, expiration date, CVC length)
        // You can use regular expressions or a library like Luhn algorithm for card number validation.

        // Example validation checks:
        if (!/^\d{16}$/.test(cardNumber)) {
        alert('Please enter a valid 16-digit card number.');
        return;
        }

        if (!/^\d{2}$/.test(expMonth) || !/^\d{4}$/.test(expYear)) {
        alert('Please enter a valid expiration date (MM/YYYY).');
        return;
        }

        if (!/^\d{3,4}$/.test(cvc)) {
        alert('Please enter a valid CVC.');
        return;
        }

        // If all validation checks pass, you can submit the form to the server.
        document.getElementById('creditCardForm').submit();
    }
    }
}
</script>

<style>

</style>