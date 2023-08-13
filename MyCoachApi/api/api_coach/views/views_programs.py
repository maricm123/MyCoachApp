from rest_framework import generics
from ..serializers.serializers_programs import TrainingProgramSerializer
from trainingProgram.models.training_program import TrainingProgram


class TrainingProgramView(generics.ListCreateAPIView):
    queryset = TrainingProgram.objects.order_by('-created_at')
    serializer_class = TrainingProgramSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        print(serializer.validated_data)
        serializer.save()
