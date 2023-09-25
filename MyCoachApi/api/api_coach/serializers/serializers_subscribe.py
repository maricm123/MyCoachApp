from django.db import transaction
from rest_framework import serializers
from api_coach.shared_serializers import PaymentMethodSerializer
from rest_framework.fields import IntegerField
from profiles.models.client import Client
from subscription.models.payment_method import PaymentMethod


class AddPaymentMethodToClientSerializer(PaymentMethodSerializer, serializers.Serializer):
    client_id = IntegerField(required=True)

    @transaction.atomic
    def validate(self, data):
        print(data, "DATA")
        try:
            payment_method = PaymentMethod.create_payment_method()
            client = Client.objects.get(id=data["client_id"])
            print(client)
            client.payment_method = payment_method
        except:
            return None
        # find client with client_id