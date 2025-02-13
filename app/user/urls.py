from django.urls import path
from user.views import CreateUSerAPIView, CrateTokenView


app_name = 'user'

urlpatterns = [
    path("create/", CreateUSerAPIView.as_view() , name= "create"),
    path("token/" , CrateTokenView.as_view(), name= "token")
]
