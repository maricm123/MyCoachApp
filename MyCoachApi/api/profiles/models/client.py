from django.conf import settings
from django.db import models


class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    payment_method = models.ForeignKey(
        "subscription.PaymentMethod",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.user.name
