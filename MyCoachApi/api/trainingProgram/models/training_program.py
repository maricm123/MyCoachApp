from django.db import models
from django.db.models import DecimalField
from profiles.models.coach import Coach
from profiles.models.client import Client
from profiles.models.sport_category import SportCategory
from django.db import transaction
from subscription.payment.stripe_handler import create_stripe_product_and_price
from rest_framework.exceptions import ValidationError
from stripe.error import StripeError


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

    price_id_stripe = models.CharField(max_length=100, blank=True, null=True)
    product_id_stripe = models.CharField(max_length=100, blank=True, null=True)

    coach_share_percentage = models.PositiveIntegerField(default=70)

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
    
    @classmethod
    @transaction.atomic
    def create(cls, name, price, pdf_file, text, sport_category, coach, coach_share_percentage):
        try:
            # Create a PaymentMethod object in your Django model (without saving it yet)
            training_program_obj = cls(
                name=name,
                price=price,
                pdf_file=pdf_file,
                text=text,
                sport_category=sport_category,
                coach_share_percentage=coach_share_percentage,
                coach=coach
            )
            # Attempt to save the PaymentMethod object in the database
            training_program_obj.save()
            stripe_training_program = create_stripe_product_and_price(name, price)
            
            training_program_obj.product_id_stripe = stripe_training_program[0]["id"]
            training_program_obj.price_id_stripe = stripe_training_program[1]["id"]

            training_program_obj.save()

        except StripeError as e:
            raise ValidationError("Error with Stripe API: " + str(e))

        except Exception as e:
            raise ValidationError("An unexpected error occurred: " + str(e))
