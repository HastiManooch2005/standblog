from django.urls import path
from ..views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(
        "activation/token/<str:token>/",
        ActivationView.as_view(),
        name="activation_token",
    ),
    path("activation/send/", ActivationSendView.as_view(), name="activation_send"),
]
