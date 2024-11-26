from rest_framework import serializers
from django.contrib.auth.hashers import make_password
import json

from ..models import Lecture
from ..models.user import User
from rest_framework.exceptions import ValidationError
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id', 'username', 'student_number', 'nickname',
            'email', 'total_point', 'major', 'school_email', 'interests'
        ]
        read_only_fields = ['total_point']

    def to_representation(self, instance):
        """
        데이터 반환 시 interests를 파싱된 리스트 형태로 변환
        """
        representation = super().to_representation(instance)

        # interests 필드가 JSON 문자열일 경우 파싱
        if isinstance(representation['interests'], str):
            try:
                representation['interests'] = json.loads(representation['interests'])
            except json.JSONDecodeError:
                representation['interests'] = []  # JSON 파싱 실패 시 기본값으로 빈 리스트 반환

        return representation

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    interests = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        min_length=1,
        max_length=10,  # 최대 10개의 관심 강의 허용
    )

    class Meta:
        model = User
        fields = [
            'username', 'student_number', 'password', 'nickname',
            'email', 'major', 'school_email','interests'
        ]

    def validate_interests(self, value):
        if len(value) != len(set(value)):
            raise ValidationError('Interest must be unique')
        if not Lecture.objects.filter(lecture_id__in=value).exists():
            raise ValidationError('One or more interests is valid')
        return value

    def save(self, **kwargs):
        hashed_password = make_password(self.validated_data['password'])
        interests = self.validated_data.pop('interests',[])

        user=super().save(password=hashed_password, **kwargs)
        user.interests = json.dumps(interests)
        user.save()
        return user