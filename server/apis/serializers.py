from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'password', 'role']
        read_only_fields = ['is_active', 'role']
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)