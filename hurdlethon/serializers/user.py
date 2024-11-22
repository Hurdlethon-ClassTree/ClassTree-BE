from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from ..models.user import User
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'STUDENT_NUMBER', 'password']

    def save(self, **kwargs):
        hashed_password=make_password(self.validated_data['password'])
        return super().save(password=hashed_password, **kwargs)
    def validate_login_id(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError("This LOGIN ID is already taken.")
        return value
