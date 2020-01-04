from rest_framework import serializers
from django.contrib.auth import get_user_model
import datetime
from django.utils import timezone

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'