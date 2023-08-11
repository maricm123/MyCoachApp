from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from ...profiles.models.client import Client
from profiles.models.client import Client
User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Overrides the default TokenObtainPairSerializer to return the user_type in the token response.
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
        read_only_fields = ('id', 'role',)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested UserSerializer

    class Meta:
        model = Client
        fields = ['user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')  # Extract user data
        print(user_data)
        user = UserSerializer().create(user_data)  # Create user instance
        client = Client.objects.create(user=user, **validated_data)
        return client