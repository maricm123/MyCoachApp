from rest_framework import serializers
from trainingProgram.models.training_program import TrainingProgram


class TrainingProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingProgram
        fields = '__all__'

