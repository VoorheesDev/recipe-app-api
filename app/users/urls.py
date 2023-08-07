from django.urls import path

from users import views


app_name = "users"

urlpatterns = [
    path("create/", views.CreateUserAPIView.as_view(), name="create"),
    path("token/", views.CreateTokenAPIView.as_view(), name="token"),
]
