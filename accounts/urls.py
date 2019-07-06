from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from .views import RegisterView

app_name = 'accounts'

urlpatterns = [
    path('auth-token/', obtain_jwt_token),
    path('refresh-token/', refresh_jwt_token),
    path('verify-token/', verify_jwt_token),
    path('signup/', RegisterView.as_view(), name="signup")
]