from django.urls import path

from users import views


app_name = "users"

urlpatterns = [
    path("create/", views.CreateUserAPIView.as_view(), name="create"),
]
