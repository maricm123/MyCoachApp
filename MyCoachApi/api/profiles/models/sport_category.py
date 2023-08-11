from django.conf import settings
from django.db import models

class SportCategory(models.Model):
    name = models.CharField(blank=False, null=False)

    def __str__(self):
        return self.name