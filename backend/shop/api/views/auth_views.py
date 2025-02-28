# backend/shop/api/views/auth_views.py
from rest_framework import generics
from shop.models import CustomUser
from shop.api.serializers.user_serializers import RegisterSerializer
from rest_framework.permissions import AllowAny

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
