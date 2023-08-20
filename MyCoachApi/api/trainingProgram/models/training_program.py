from django.db import models
from django.db.models import DecimalField
from profiles.models.coach import Coach
from profiles.models.client import Client
from profiles.models.sport_category import SportCategory


class TrainingProgram(models.Model):
    name = models.CharField()
    price = DecimalField(max_digits=9, decimal_places=2)
    pdf_file = models.FileField(upload_to='pdfs/', blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    sport_category = models.ForeignKey(
        SportCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    coach = models.ForeignKey(
        Coach, on_delete=models.CASCADE, related_name='tweets', blank=False, null=False)

    clients = models.ManyToManyField(
        Client, blank=True, related_name='bought_programs'
    )

    # MONTHLY = 'monthly'
    # YEARLY = 'yearly'
    # LIFETIME = 'lifetime'

    # TYPE_SUB_CHOICES = [
    #     (MONTHLY, 'Monthly'),
    #     (YEARLY, 'Yearly'),
    #     (LIFETIME, 'Lifetime'),
    # ]
    #
    # type_subscription = models.CharField(max_length=10, choices=TYPE_SUB_CHOICES, default=MONTHLY)

    def __str__(self):
        return self.name
