from django.contrib import admin
from django.contrib.auth import get_user_model
from .models.subscribe import Subscribe
from .models.coach_transaction import CoachTransaction


admin.site.register(Subscribe)
admin.site.register(CoachTransaction)

