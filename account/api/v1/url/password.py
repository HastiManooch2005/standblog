from django.urls import path
from ..views import *


urlpatterns = [
    path("change/pass", ChangePasswordView.as_view(), name="change_password"),
    path("email", SendMail.as_view(), name="email"),
]
