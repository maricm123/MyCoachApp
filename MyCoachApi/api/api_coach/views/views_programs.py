from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from ..serializers.serializers_programs import TrainingProgramSerializer
from trainingProgram.models.training_program import TrainingProgram

from profiles.models.user import User


class TrainingProgramView(generics.ListCreateAPIView):
    queryset = TrainingProgram.objects.order_by('-created_at')
    serializer_class = TrainingProgramSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()


class TrainingProgramsListByUser(generics.ListAPIView):
    # User profile - tvitovi samo od usera
    serializer_class = TrainingProgramSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the user ID from the URL parameter
        user_id = self.kwargs.get('pk')
        # Retrieve the user object from the database
        user = get_object_or_404(User, id=user_id)
        return TrainingProgram.objects.filter(user=user).order_by('-created_at')


class TrainingProgramDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TrainingProgram.objects.all()
    serializer_class = TrainingProgramSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

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
