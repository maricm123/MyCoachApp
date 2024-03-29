import stripe
from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from ..serializers.serializers_programs import TrainingProgramSerializer, TrainingProgramSerializerForCreate
from trainingProgram.models.training_program import TrainingProgram
from profiles.models.coach import Coach
from profiles.models.user import User
from subscription.payment.stripe_handler import create_stripe_product_and_price
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

stripe.api_key = settings.STRIPE_SECRET_KEY


class TrainingProgramView(generics.ListCreateAPIView):
    queryset = TrainingProgram.objects.order_by('-created_at')
    serializer_class = TrainingProgramSerializer


class TrainingProgramCreate(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = TrainingProgramSerializerForCreate(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=HTTP_201_CREATED)


class TrainingProgramsListByUser(generics.ListAPIView):
    serializer_class = TrainingProgramSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        user = get_object_or_404(User, id=user_id)
        return TrainingProgram.objects.filter(user=user).order_by('-created_at')


class TrainingProgramDetail(generics.RetrieveUpdateDestroyAPIView):
    """
        View to get details and update training program
    """

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
    """
        View to get just training list for logged coach
    """
    serializer_class = TrainingProgramSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return TrainingProgram.objects.filter(coach__user=user).order_by('-created_at')
