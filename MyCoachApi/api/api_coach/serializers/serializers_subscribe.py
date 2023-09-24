from django.db import transaction
from rest_framework import serializers
from api_coach.shared_serializers import PaymentMethodSerializer
from rest_framework.fields import IntegerField


class AddPaymentMethodToClientSerializer(PaymentMethodSerializer, serializers.Serializer):
    client_id = IntegerField()
    @transaction.atomic
    def validate(self, data):
        print(data, "DATA")
        try:
            # payment_method = PaymentMethod.objects.create()
            client = Client.objects.get(id=data["client_id"])
            print(client)
            client.payment_method = payment_method
        # find client with client_id