from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password

from .models import User, Category, Course
from .mixins import ModelSerializerMixin, TagSerializer


class SetPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    def validate(self, value):
        user = self.context['request'].user
        if not check_password(value, user.password):
            raise serializers.ValidationError("Current password is incorrect.")
        return value


class UserSerializer(ModelSerializerMixin):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ModelSerializerMixin.Meta.fields + ['username', 'email', 'password', 'first_name', 'last_name', 'role', 'avatar']
        read_only_fields = ModelSerializerMixin.Meta.read_only_fields + ['role']
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    
class CategorySerializer(ModelSerializerMixin):
    class Meta:
        model = Category
        fields = ModelSerializerMixin.Meta.fields + ['name']
        
        
class CourseSerializer(TagSerializer):
    category = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Course
        fields = TagSerializer.Meta.fields + ['name', 'price', 'category']