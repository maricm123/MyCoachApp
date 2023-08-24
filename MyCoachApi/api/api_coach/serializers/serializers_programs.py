from rest_framework import serializers
from trainingProgram.models.training_program import TrainingProgram
from api_coach.serializers.serializers_profiles import CoachSerializer
from api_coach.serializers.serializers_profiles import SportCategorySerializer


class TrainingProgramSerializer(serializers.ModelSerializer):
    coach = CoachSerializer()
    sport_category = SportCategorySerializer()

    class Meta:
        model = TrainingProgram
        fields = ['id', 'name', 'price', 'pdf_file', 'text',
                  'created_at', 'clients', 'coach', 'sport_category', 'price_id_stripe',]

