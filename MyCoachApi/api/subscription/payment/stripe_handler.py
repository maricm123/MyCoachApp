import stripe
from subscription.payment.stripe import (
    create_stripe_customer_id,
    attach_stripe_card,
    create_stripe_product,
    create_stripe_price,
    create_stripe_subscription,
    create_stripe_payment_method,
    attach_stripe_payment_method,
    detach_stripe_card_from_id,
    list_stripe_payment_methods,
    set_default_stripe_payment_method
)
from django.conf import settings
from stripe.error import StripeError
from rest_framework.response import Response
from subscription.utils import usd_to_cents
from rest_framework.exceptions import ValidationError


def create_stripe_customer(email):
    try:
        # Create a new customer object
        customer = create_stripe_customer_id(email)
        return customer.stripe_id

    except Exception as e:
        print(e, "EXCEPTION STIRPE HANDLER")
        # Handle the exception if needed
        return None


def create_payment_method(customer_id, token):
    try:
        payment_method = create_stripe_payment_method(token)

        # Attach the Payment Method to the customer
        attach_stripe_payment_method(payment_method.id, customer_id)
        return payment_method

    except stripe.error.StripeError as e:
        # Handle Stripe API errors here
        print(f"Stripe error: {e}")
        return None
    

def create_stripe_product_and_price(name, price):
    try:
        stripe_product = create_stripe_product(name)
        
        cent_price = usd_to_cents(price)
        stripe_price = create_stripe_price(cent_price, stripe_product)

        return stripe_product, stripe_price

    except StripeError as e:
        raise ValidationError({'error': str(e)}, status=400)
    

def create_subscription(client, program):
    try:
        subscription = create_stripe_subscription(client, program)
        return subscription
    except StripeError as e:
        raise ValidationError({'error': str(e)}, status=400)
        

def list_payment_methods(customer_id):
    try:
        payment_methods = list_stripe_payment_methods(customer_id)
        return payment_methods

    except stripe.error.StripeError as e:
        # Handle Stripe API errors here
        print(f"Stripe error: {e}")
        return None
    

def set_default_payment_method(customer_id, payment_method_id):
    try:
        set_default_stripe_payment_method(customer_id, payment_method_id)
        return True

    except stripe.error.StripeError as e:
        # Handle Stripe API errors here
        print(f"Stripe error: {e}")
        return False


def detach_payment_card_from_id(card_id):
    try:
        detach_stripe_card_from_id(card_id)
        return True
    except StripeError as e:
        return Response({'error': str(e)}, status=400)