import stripe
from subscription.payment.stripe import create_stripe_customer_id
from django.conf import settings


def create_stripe_customer(email):
    try:
        # Create a new customer object
        customer = create_stripe_customer_id(email)
        return customer.stripe_id

    except Exception as e:
        print(e, "EXCEPTION STIRPE HANDLER")
        # Handle the exception if needed
        return None

