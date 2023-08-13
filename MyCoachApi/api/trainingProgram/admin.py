from django.contrib import admin
from django.contrib.auth import get_user_model
from .models.training_program import TrainingProgram


admin.site.register(TrainingProgram)
