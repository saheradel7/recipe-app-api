from user.serializers import UserSerializer,AuthTokenSerializer

from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

class CreateUSerAPIView(generics.CreateAPIView):
    
    serializer_class = UserSerializer
    

class CrateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes= api_settings.DEFAULT_RENDERER_CLASSES #optional