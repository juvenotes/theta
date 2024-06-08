from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = [ # noqa: RUF012
            "id",
            "username", 
            "email",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
            "created",
            "modified",
            "last_login",
        ]
        read_only_fields = ["id", "is_active", "is_staff", "is_superuser", "created", "modified", "last_login"]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class AdditionalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['role', 'graduation_year', 'student_profession', 'institution']

class CustomTokenObtainPairSerializer(serializers.Serializer):
    def validate(self, attrs):
        user = self.context['request'].user
        refresh = RefreshToken.for_user(user)

        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return data

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.username
        # ...

        return token