from django.db import models
from profiles.models.client import Client
from trainingProgram.models.training_program import TrainingProgram


class SubscribeManager(models.Manager):
    def subscribes_by_client(self, client):
        return self.filter(client__isnull=False)


class Subscribe(models.Model):
    # ManyToOne
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

    created_at = models.DateTimeField(auto_now_add=True)

    current_period_end = models.DateTimeField(blank=False, null=False)

    coach_share_percentage = models.IntegerField()

    stripe_subscription_id = models.CharField(blank=False, null=False)

    status = models.CharField(null=True, blank=True, max_length=100)

    objects = SubscribeManager()

    def __str__(self):
        return f"{self.client} - {self.training_program}"