from django.db import transaction
from rest_framework import serializers
from api_coach.shared_serializers import PaymentMethodSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField
from profiles.models.client import Client
from stripe.error import StripeError
from subscription.models.payment_method import PaymentMethod


class AddPaymentMethodToClientSerializer(PaymentMethodSerializer, serializers.Serializer):
    client_id = serializers.IntegerField(required=True)
    token = serializers.CharField(required=True)

    def validate_client_id(self, value):
        try:
            client = Client.objects.get(id=value)
        except Client.DoesNotExist:
            raise serializers.ValidationError("Client does not exist")
        return client

    def validate(self, data):
        card_number = data["number"]
        exp_month = data["exp_month"]
        exp_year = data["exp_year"]
        cvc = data["cvc"]
        client = data["client_id"]
        token = data["token"]
        try:
            PaymentMethod.create(client, client.stripe_customer_id, card_number, exp_month, exp_year, cvc, token)
            return data
        except StripeError as e:
            raise ValidationError("Stripe error occurred", e)
