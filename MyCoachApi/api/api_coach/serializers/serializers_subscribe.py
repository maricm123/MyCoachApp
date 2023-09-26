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
        # ovde izvadim podatke iz 'data'
        # mozda i vaditi usera iz request.data.user
        print(data, "DATA")
        try:
            # ovde nadjem clienta, izvadim njegov stripe_id 
            client = Client.objects.get(id=data["client_id"])
            print(client)

            # kreiramo objekat payment method i dodajemo klijentu 
            payment_method = PaymentMethod.create()
            client.payment_method = payment_method
        except:
            return None
        # find client with client_id