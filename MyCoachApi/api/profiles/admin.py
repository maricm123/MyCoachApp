from django.contrib import admin
from django.contrib.auth import get_user_model
from .models.coach import Coach
from .models.client import Client
from .models.sport_category import SportCategory

User = get_user_model()

admin.site.register(User)
admin.site.register(Coach)
admin.site.register(Client)
admin.site.register(SportCategory)