from rest_framework import serializers
from .models import CustomUser

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone', 'city', 'avatar']
