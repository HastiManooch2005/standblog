from django.urls import include, path

urlpatterns = [
    path("", include("account.api.v1.url.token")),
    path("", include("account.api.v1.url.password")),
]
