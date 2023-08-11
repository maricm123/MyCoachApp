from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import include, path
from .views import views_profiles
app_name = "api_coach"

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('user/login/', views_profiles.UserLoginView.as_view(), name='user_login'),
    path('client/register/', views_profiles.ClientUserRegisterView.as_view(), name='client_register'),
]
