from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from ..models.user import User
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'student_number', 'password', 'nickname',
            'email', 'total_point', 'major', 'school_email', 'interests'
        ]

    def save(self, **kwargs):
        hashed_password = make_password(self.validated_data['password'])
        return super().save(password=hashed_password, **kwargs)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError("This username is already taken.")
        return value
