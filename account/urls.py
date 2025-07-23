from django.urls import path
from . import views
from django.urls import include

app_name = "account"
urlpatterns = [
    path("login", views.user_login, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("edit", views.edit, name="edit"),
    path("api/v1/", include("account.api.v1.url")),
    path("api/v2/", include("djoser.urls.jwt")),  # migration  v1 to v2
]
