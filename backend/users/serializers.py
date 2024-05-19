from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

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
        extra_kwargs = {'password': {'write_only': True}}

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