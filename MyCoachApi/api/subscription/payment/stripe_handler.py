import stripe
from subscription.payment.stripe import (
    create_stripe_customer_id,
    attach_stripe_card,
    create_stripe_product,
    create_stripe_price,
    create_stripe_subscription
)
from django.conf import settings
from stripe.error import StripeError
from rest_framework.response import Response

def create_stripe_customer(email):
    try:
        # Create a new customer object
        customer = create_stripe_customer_id(email)
        return customer.stripe_id

    except Exception as e:
        print(e, "EXCEPTION STIRPE HANDLER")
        # Handle the exception if needed
        return None


# We are using here payment method API
def attach_stripe_card(stripe_id, payment_method):
    try:
        card = attach_stripe_card(stripe_id=stripe_id, payment_method=payment_method)
        print(card)
        return card
    except Exception as e:
        print(e, "EXCEPTION STIRPE HANDLER")
        # Handle the exception if needed
        return None
    

def create_payment_method(type, number, exp_month, exp_year, cvc):
    try:
        pass


    except Exception as e:
        print(e, "EXCEPTION CREATE PAYMENT METHOD")
        return None
    

def create_stripe_product_and_price(name, price):
    try:
        product = create_stripe_product(name)
        price = create_stripe_price(price, product)
        return product.id
    except StripeError as e:
        return Response({'error': str(e)}, status=400)
    

def create_subscription(client, program):
    try:
        subscription = create_stripe_subscription(client, program)
        return subscription
    except StripeError as e:
        return Response({'error': str(e)}, status=400)
        

    