from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import include, path
from .views import views_profiles, views_programs
app_name = "api_coach"

urlpatterns = [
    # AUTHENTICATION
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/login/', views_profiles.UserLoginView.as_view(), name='user_login'),
    path('coach/register/', views_profiles.CoachRegisterView.as_view(), name='coach_register'),
    path('client/register/', views_profiles.ClientRegisterView.as_view(), name='client_register'),
    # TRAINING PROGRAMS
    path('program/', views_programs.TrainingProgramView.as_view(), name='training_program'),
]
