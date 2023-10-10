from rest_framework import serializers
from profiles.models.coach import Coach
from trainingProgram.models.training_program import TrainingProgram
from api_coach.serializers.serializers_profiles import CoachSerializer
from api_coach.serializers.serializers_profiles import SportCategorySerializer

class DateFromDateTimeField(serializers.ReadOnlyField):
    def __init__(self, date_format=None, *args, **kwargs):
        self.date_format = date_format
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        if value:
            return value.strftime(self.date_format)
        return None

class TrainingProgramSerializer(serializers.ModelSerializer):
    coach = CoachSerializer()
    sport_category = SportCategorySerializer()
    created_at = DateFromDateTimeField(date_format='%d-%m-%Y')  # Define your desired format here

    class Meta:
        model = TrainingProgram
        fields = ['id', 'name', 'price', 'pdf_file', 'text',
                  'created_at', 'clients', 'coach', 'sport_category', 'price_id_stripe',]

        read_only_fields = ['price_id_stripe',]


class TrainingProgramSerializerForCreate(serializers.ModelSerializer):
    coach = serializers.CharField(required=True)

    class Meta:
        model = TrainingProgram
        fields = ['name', 'price', 'pdf_file', 'text', 'coach_share_percentage', 'sport_category', 'coach', ]
    
    def validate_coach(self, value):
        try:
            coach = Coach.objects.get(user_id=value)
        except Coach.DoesNotExist:
            raise serializers.ValidationError("Coach does not exist")
        return coach
            
    def validate(self, data):
        TrainingProgram.create(**data)
        return data