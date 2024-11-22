from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from ..models.user import User
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'STUDENT_NUMBER',
                  'password','NICKNAME' ,'email', 'TOTAL_POINT', 'MAJOR', 'SCHOOL_EMAIL', 'INTERESTS']
    def save(self, **kwargs):
        hashed_password=make_password(self.validated_data['password'])
        # kwargs["username"] = self.validated_data["USERNAME"]
        return super().save(password=hashed_password, **kwargs)
    def validate_login_id(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError("This LOGIN ID is already taken.")
        return value
