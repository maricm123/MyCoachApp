from django.db import models

from profiles.models.client import Client

from trainingProgram.models.training_program import TrainingProgram


class Subscribe(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    training_program = models.ForeignKey(
        TrainingProgram,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    coach_share_percentage = models.IntegerField()

    stripe_subscription_id = models.CharField(blank=False, null=False)

    status = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return f"{self.client} - {self.training_program}"