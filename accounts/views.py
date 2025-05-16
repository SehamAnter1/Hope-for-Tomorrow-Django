from django.shortcuts import render
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import RegisterSerializer

User = get_user_model()
# ________ Register View ________
class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class= RegisterSerializer
    permission_classes = [permissions.AllowAny]

    

# ________ Login View (using SimpleJWT) ________
class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer 
    permission_classes = [permissions.AllowAny]


# ________ Reset Password View ________
class SendResetPasswordEmailView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
