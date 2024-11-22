from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from ..models.user import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'STUDENT_NUMBER', 'password']

    def save(self, **kwargs):
        hashed_password=make_password(self.validated_data['password'])
        return super().save(password=hashed_password, **kwargs)