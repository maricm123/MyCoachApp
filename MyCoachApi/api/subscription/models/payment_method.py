from django.db import models


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
