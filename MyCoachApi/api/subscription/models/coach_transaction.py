from django.db import models
from profiles.models.coach import Coach
from .subscribe import Subscribe


class CoachTransaction(models.Model):
    coach = models.ForeignKey(
        Coach,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    subscription = models.ForeignKey(
        Subscribe,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    amount = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Subscription = {self.subscription} ----Coach - '{self.coach}' -Amount -'{self.amount}'"
