from django.db import models
from django.db import transaction
from subscription.payment.stripe_handler import create_payment_method

class PaymentMethod(models.Model):
    """
    Model just for Card
    PaymentMethodAPI on Stripe
    """
    type = models.CharField(max_length=50, null=False, blank=False, default="card")
    number = models.CharField(max_length=16)  # Assuming 16-digit card number
    exp_month = models.PositiveIntegerField()
    exp_year = models.PositiveIntegerField()
    cvc = models.CharField(max_length=4)

    def __str__(self):
        return f"Card ending in {self.number[-4:]}"


    @classmethod
    @transaction.atomic
    def create(cls, customer_id, number, exp_month, exp_year, cvc):
        try:
            # Create Stripe PaymentMethod
            payment_method = create_payment_method(customer_id, number, exp_month, exp_year, cvc)

            # Create a PaymentMethod object in your Django model
            payment_method_obj = cls(
                type="card",
                number=number,
                exp_month=exp_month,
                exp_year=exp_year,
                cvc=cvc,
            )
            payment_method_obj.save()

            return payment_method_obj

        # except stripe.error.StripeError as e:
        except Exception as e:
            # Handle Stripe API errors here
            print(f"Stripe error: {e}")
            return None
        
    # def attach_to_customer(self, customer_id):
    #     try:
    #         # Attach the PaymentMethod to the customer
    #         attach = attach_stripe_card(customer_id, self)
    #         print(attach)
    #         return True

    #     # except stripe.error.StripeError as e:
    #     except Exception as e:
    #         # Handle Stripe API errors here
    #         print(f"Stripe error: {e}")
    #         return False