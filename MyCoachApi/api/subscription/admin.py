from django.contrib import admin
from .models.subscribe import Subscribe
from .models.coach_transaction import CoachTransaction
from .models.payment_method import PaymentMethod

admin.site.register(Subscribe)
admin.site.register(CoachTransaction)
admin.site.register(PaymentMethod)

