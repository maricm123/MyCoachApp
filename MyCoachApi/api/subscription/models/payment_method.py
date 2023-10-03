from typing import Any
from django.db import models, IntegrityError
from django.db import transaction
from rest_framework.exceptions import ValidationError
from stripe.error import StripeError
from subscription.payment.stripe_handler import create_payment_method
from profiles.models.client import Client


class PaymentMethodManager(models.Manager):
    def get_payment_methods_for_client(self, client):
        """
        Get all PaymentMethods associated with a specific client
        """
        return self.filter(client=client)


class PaymentMethod(models.Model):
    """
    Model just for Card
    PaymentMethodAPI on Stripe
    """
    # When client is deleted, all associated PaymentMethods objects are deleted.
    # ManyToOne
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='payment_methods')
    type = models.CharField(max_length=50, null=False, blank=False, default="card")
    number = models.CharField(max_length=16)  # Assuming 16-digit card number
    exp_month = models.PositiveIntegerField()
    exp_year = models.PositiveIntegerField()
    cvc = models.CharField(max_length=4)
    stripe_payment_method_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Card ending in {self.number[-4:]}"
    
    class Meta:
        unique_together = ('client', 'number')  # Ensure uniqueness based on client and card number

    # Custom manager
    objects = PaymentMethodManager()

    @classmethod
    @transaction.atomic
    def create(cls, client, customer_id, number, exp_month, exp_year, cvc, token):
        try:
            # Create Stripe PaymentMethod
            stripe_payment_method = create_payment_method(customer_id, token)
            stripe_payment_method_id = stripe_payment_method.id

            # Create a PaymentMethod object in your Django model
            payment_method_obj = cls(
                client=client,
                type="card",
                number=number,
                exp_month=exp_month,
                exp_year=exp_year,
                cvc=cvc,
                stripe_payment_method_id=stripe_payment_method_id,
            )
            payment_method_obj.save()

            return payment_method_obj

        except StripeError as e:
            raise ValidationError("Nesto ne valja u create", e)

        except IntegrityError:
            raise ValidationError("Ne moze dve iste kartice jedan korisnik")


    # Here we need to see if that card is default for client
    @property
    def is_default(self) -> bool:
        return self == self.client.default_card
