from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from custom_auth.views import RegisterView

urlpatterns = [

    path("login", TokenObtainPairView.as_view(), name='login'),
    path("refresh-token", TokenRefreshView.as_view(), name='refresh-token'),
    path("register", RegisterView.as_view(), name='register'),

]
