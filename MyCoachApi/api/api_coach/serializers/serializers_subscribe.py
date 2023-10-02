from django.db import transaction
from subscription.payment.stripe_handler import list_payment_methods
from rest_framework import serializers
from api_coach.shared_serializers import PaymentMethodSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField
from profiles.models.client import Client
from stripe.error import StripeError
from subscription.models.payment_method import PaymentMethod
from django.shortcuts import get_object_or_404


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


class GetClientPaymentMethodsSerializer(serializers.Serializer):

    def validate(self, data):
        print(data)
        
        # client = get_object_or_404(Client, user=self.request.user)
        # verovatno mi ne treba stripe ovde, samo cu izvuci kartice iz baze
            # customer_id = client.customer_id
            # card_list = #list_payment_methods(customer_id=customer_id)

        return data