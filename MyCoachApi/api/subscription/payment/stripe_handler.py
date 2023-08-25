import stripe
from subscription.payment.stripe import create_stripe_customer
from django.conf import settings


class StripeHelper:
    def create_stripe_customer(self, email):
        try:
            # Create a new customer object
            customer = create_stripe_customer(email)
            print(customer)
            print(customer.stripe_id)
            return customer.stripe_id

        except Exception as e:
            print(e, "EXCEPTION STIRPE HANDLER")
            # Handle the exception if needed
            return None
