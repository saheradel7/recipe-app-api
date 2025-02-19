from django.urls import path
from user.views import (
    CreateUserAPIView,
    CreateTokenView,
    RetrieveUpdateUserAPIView
)


app_name = "user"

urlpatterns = [
    path("create/", CreateUserAPIView.as_view(), name="create"),
    path("token/", CreateTokenView.as_view(), name="token"),
    path("me/", RetrieveUpdateUserAPIView.as_view(), name="me"),
]
