# backend/shop/api/serializers/user_serializers.py
from rest_framework import serializers
from shop.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'role')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'role')

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data.get('role', 'customer')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
