from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import include, path
from .views import views_profiles, views_programs, views_subscriptions
app_name = "api_coach"

urlpatterns = [
    # AUTHENTICATION
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/login/', views_profiles.UserLoginView.as_view(), name='user_login'),
    path('coach/register/', views_profiles.CoachRegisterView.as_view(), name='coach_register'),
    path('client/register/', views_profiles.ClientRegisterView.as_view(), name='client_register'),
    path('current-user/', views_profiles.CurrentUserView.as_view(),
             name='current-user'),

    path('logout/', views_profiles.LogoutView.as_view(), name='logout'),
    path('my-profile/<int:pk>/',
         views_profiles.MyProfileView.as_view(), name='my_profile'),

    # TRAINING PROGRAMS
    path('program/', views_programs.TrainingProgramView.as_view(), name='training-program'),
    path('program/<int:pk>/', views_programs.TrainingProgramDetail.as_view(), name='training-detail'),
    path('programs-by-me/', views_programs.TrainingListByMe.as_view(), name='trainings-by-me'),
    path('create-program/', views_programs.TrainingProgramCreate.as_view(), name='create-program'),
    # SPORT CATEGORIES
    path('sport-categories/', views_profiles.SportCategoriesListView.as_view(), name='sport-categories'),


    # SUBSCRIPTIONS
    path('add-payment-method-to-client/', views_subscriptions.AddPaymentMethodToClientView.as_view(), name='add-payment-method-to-client'),
    path('create-subscription/', views_subscriptions.CreateSubscription.as_view(), name='create-subscription'),
    path('webhook-test/' , views_subscriptions.WebHook.as_view()),
]
