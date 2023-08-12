from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from ..serializers.serializers_profiles import CustomTokenObtainPairSerializer, CoachSerializer, \
    ClientSerializer

User = get_user_model()


class UserLoginView(TokenObtainPairView):
    """
    View to handle login
    """
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data)


class CoachRegisterView(generics.CreateAPIView):
    """
    View to handle registration of Users.
    """
    serializer_class = CoachSerializer

    def perform_create(self, serializer):
        # Call the default perform_create() method to handle user registration
        user = serializer.save()
        # Return a response indicating successful registration
        return Response({'message': 'User registered successfully.'})


class ClientRegisterView(generics.CreateAPIView):
    """
    View to handle registration of Users.
    """
    serializer_class = ClientSerializer

    def perform_create(self, serializer):
        # Call the default perform_create() method to handle user registration
        user = serializer.save()
        # Return a response indicating successful registration
        return Response({'message': 'User registered successfully.'})