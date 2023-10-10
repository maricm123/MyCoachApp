from django.db import transaction
from .serializers_programs import TrainingProgramSerializer
from subscription.models.subscribe import Subscribe
from api_coach.mixins import ReqContextMixin
from subscription.payment.stripe_handler import list_payment_methods
from rest_framework import serializers
from api_coach.shared_serializers import PaymentMethodSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField
from profiles.models.client import Client
from stripe.error import StripeError
from subscription.models.payment_method import PaymentMethod
from django.shortcuts import get_object_or_404
from ..shared_serializers import DateFromDateTimeField

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


class DefaultCardSerializer(ReqContextMixin, serializers.Serializer):
    """
    WARN: This serializer has no fields data, it is just used as a proxy to get Stripe infos.
    """
    payment_method_id = serializers.CharField(required=True)

    def validate_payment_method_id(self, value):
        try:
            payment_method = PaymentMethod.objects.get(id=value)
        except PaymentMethod.DoesNotExist:
            raise serializers.ValidationError("Payment method does not exist")
        return payment_method

    def validate(self, data):
        client = get_object_or_404(Client, user=self._req_context.user)
        payment_method = data["payment_method_id"]
        client.set_default_card(payment_method)
        return data
    

class ClientSubscribeListSerializer(serializers.ModelSerializer):
    training_program = TrainingProgramSerializer()
    created_at = DateFromDateTimeField(date_format='%d-%m-%Y')
    current_period_end = DateFromDateTimeField(date_format='%d-%m-%Y')
    
    class Meta:
        model = Subscribe
        fields = ("training_program", "created_at", "current_period_end",)
