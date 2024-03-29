from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from profiles.models.client import Client
from profiles.models.coach import Coach
from profiles.models.sport_category import SportCategory

from api_coach.shared_serializers import PaymentMethodSerializer

User = get_user_model()


class SportCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SportCategory
        fields = '__all__'


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Overrides the default TokenObtainPairSerializer to return the role in the token response.
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        access = refresh.access_token
        data['role'] = self.user.role
        data['refresh'] = str(refresh)
        data['access'] = str(access)
        return data


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the base User model.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'password', 'email',
                  'role',)

        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CoachSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested UserSerializer
    sport_category = SportCategorySerializer(required=False)

    class Meta:
        model = Coach
        fields = ['user', 'biography', 'sport_category', ]
        read_only_fields = ["sport_category", ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer().create(user_data)  # Create user instance
        coach = Coach.objects.create(user=user, **validated_data)
        return coach


class ClientSerializer(UserSerializer, serializers.Serializer):
    @transaction.atomic
    def validate(self, data):
        user = User.objects.create_user(name=data["name"], email=data["email"], password=data["password"])
        client = Client.create(user=user)
        return client


class SportCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportCategory
        fields = '__all__'



