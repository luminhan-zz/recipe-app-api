from django.shortcuts import render
from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework import generics, permissions, authentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """update authenticated user profile"""
    # ဒီမှာ PUT ရယ် PATCH ရယ်ကိုလက်ခံတယ်။ PUT က user object တစ်ခုလုံးကို
    # update လုပ်တာ။ အဲ့တော့ create လုပ်ရင် လိုတဲ့ required field တွေ အကုန်
    # ထည့်ပေးဖို့လိုတယ်။
    # PATCH ကကျ request မှာ ထည့်ပေးလိုက် တဲ့ field ကိုပဲ update လုပ်တာ။
    # field တွေအကုန်ထည့်ပေးစရာမလိုဘူး။

    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get_object(self):
        return self.request.user

