import stripe
from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from stripe.error import StripeError

from ..serializers.serializers_programs import TrainingProgramSerializer, TrainingProgramSerializerForCreate
from trainingProgram.models.training_program import TrainingProgram
from profiles.models.coach import Coach

from profiles.models.user import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class TrainingProgramView(generics.ListCreateAPIView):
    queryset = TrainingProgram.objects.order_by('-created_at')
    serializer_class = TrainingProgramSerializer


class TrainingProgramCreate(generics.CreateAPIView):
    serializer_class = TrainingProgramSerializerForCreate
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        with transaction.atomic():
            try:
                name = self.request.data['name']
                price = self.request.data['price']
                stripe_product = create_stripe_product(self, name, price)
                coach = Coach.objects.get(user=self.request.user)
                serializer.save(coach=coach, price_id_stripe=stripe_product)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def create_stripe_product(self, name, price):
    try:
        product = stripe.Product.create(name=name)
        price = stripe.Price.create(
            unit_amount=price,
            currency="usd",
            product=product.id,
        )
        return product.id
    except StripeError as e:
        return Response({'error': str(e)}, status=400)


class TrainingProgramsListByUser(generics.ListAPIView):
    serializer_class = TrainingProgramSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        user = get_object_or_404(User, id=user_id)
        return TrainingProgram.objects.filter(user=user).order_by('-created_at')


class TrainingProgramDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TrainingProgram.objects.all()
    serializer_class = TrainingProgramSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        training = self.get_object()
        if training.user == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied(
                "You do not have permission to update this training.")

    def perform_destroy(self, instance):
        training = self.get_object()
        if training.user == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied(
                "You do not have permission to delete this training.")


class TrainingListByMe(generics.ListAPIView):
    # User profile - tvitovi samo od usera koji je ulogovan
    serializer_class = TrainingProgramSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return TrainingProgram.objects.filter(coach__user=user).order_by('-created_at')
