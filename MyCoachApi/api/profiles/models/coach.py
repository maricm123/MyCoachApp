from django.conf import settings
from django.db import models
from .sport_category import SportCategory


class Coach(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    biography = models.TextField(blank=True, null=True)

    sport_category = models.ForeignKey(
        SportCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=SportCategory._meta.verbose_name,
    )

    def __str__(self):
        return self.user.name