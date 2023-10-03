from django.conf import settings
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from subscription.payment.stripe_handler import create_stripe_customer


class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    default_card = models.ForeignKey(
        "subscription.PaymentMethod",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Default card"),
        related_name='client_default_payment_method'
    )

    def __str__(self):
        return self.user.name
    
    def set_default_card(self, card):
        self.default_card = card
        self.save()

    # def get_default_card(self):
    #     if self.default_card_id is not None:
    #         return PaymentMethod.objects.get(id=self.default_card_id)
    #     return None

    @classmethod
    @transaction.atomic
    def create(cls, user):
        """
        Create a new Client instance linked to the provided user, and create
            Customer on Stripe
        """
        client = cls(user=user)
        stripe_customer_id = create_stripe_customer(email=user.email)
        client.stripe_customer_id = stripe_customer_id
        client.save()
        return client
