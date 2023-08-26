import stripe
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from rest_framework import generics, status, request
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from ..serializers.serializers_profiles import CustomTokenObtainPairSerializer, CoachSerializer, \
    ClientSerializer, UserSerializer, SportCategoriesSerializer
from profiles.models.coach import Coach
from profiles.models.client import Client
from profiles.models.sport_category import SportCategory
from django.conf import settings

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

    @transaction.atomic
    def perform_create(self, serializer):
        # Call the default perform_create() method to handle user registration
        client = serializer.save()
        try:
            stripe_id = create_stripe_customer(client.user.email)
            client.stripe_customer_id = stripe_id
            client.save()
        except Exception as e:
            print(e)
        # Return a response indicating successful registration
        return Response({'message': 'User registered successfully.'})


class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MyProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        if user.role == 'coach':
            coach = Coach.objects.get(user=user)
            serializer = CoachSerializer(coach)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if user.role == 'client':
            client = Client.objects.get(user=user)
            serializer = ClientSerializer(client)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, asd):
        user = self.get_object()

        # Check if the user is the same as the authenticated user
        if user == self.request.user:
            if user.user_type == 'client':
                client = Client.objects.get(
                    user=user)
            #     # pass request data to the serializer instance
            #     serializer = BusinessUserSerializerForUpdate(
            #         business_user, data=self.request.data)
            #     serializer.is_valid(raise_exception=True)
            #     # Ensure data is valid
            #     serializer.save()
            #     return Response(serializer.data, status=status.HTTP_200_OK)
            # elif user.user_type == 'default':
            #     default_user = DefaultUser.objects.get(user=user)
            #     # pass request data to the serializer instance
            #     serializer = DefaultUserSerializerForUpdate(
            #         default_user, data=self.request.data)
            #     serializer.is_valid(raise_exception=True)
            #     # Ensure data is valid
            #     serializer.save()
            #     return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise ValidationError("Invalid user type")
        else:
            raise PermissionDenied(
                "You do not have permission to update this user.")


def create_stripe_customer(email):
    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY  # Replace with your Stripe Secret Key
        # Create a new customer object
        customer = stripe.Customer.create(email=email)
        return customer.id

    except Exception as e:
        print(e)
        # Handle the exception if needed
        return None


class SportCategoriesListView(generics.ListAPIView):
    serializer_class = SportCategoriesSerializer
    queryset = SportCategory.objects.all()
