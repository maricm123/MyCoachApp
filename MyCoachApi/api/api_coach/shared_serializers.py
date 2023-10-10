from rest_framework import serializers
from subscription.models import PaymentMethod
from rest_framework import fields as rest_fields


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'
        read_only_fields = ['type', 'client',]


class ListPaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ("id", "type", "number", "exp_month", "exp_year", "cvc", "is_default")

    # is default is property in PaymentMethod object
    is_default = rest_fields.BooleanField()


class DateFromDateTimeField(serializers.ReadOnlyField):
    def __init__(self, date_format=None, *args, **kwargs):
        self.date_format = date_format
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        if value:
            return value.strftime(self.date_format)
        return None