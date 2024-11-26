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


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        lectures = Lecture.objects.all()
        choices=[(lecture.lecture_id, lecture.lecture_name) for lecture in lectures]
        lecture_count=Lecture.objects.count()
        max_fields = min(lecture_count, 10)  # 최대 10개 필드 생성

        # 필드 동적으로 추가
        for i in range(max_fields):
            self.fields[f'interest_{i + 1}'] = serializers.ChoiceField(
                choices=choices,
                write_only=True,
                required=False,
                allow_null=True,
                help_text=f"Select Lecture ID for interest {i + 1}"
            )

    # interests = serializers.ListField(
    #     child=serializers.IntegerField(),
    #     write_only=True,
    #     min_length=1,
    #     max_length=10,  # 최대 10개의 관심 강의 허용
    # )

    class Meta:
        model = User
        fields = [
            'username', 'student_number', 'password', 'nickname',
            'email', 'major', 'school_email'
        ]

    def create(self, validated_data):
        # 동적 관심 강의 필드에서 데이터를 수집
        lecture_ids = []
        for i in range(10):
            key = f'interest_{i + 1}'
            if key in validated_data:
                value = validated_data.pop(key)
                if value is not None:
                    lecture_ids.append(value)

        # 중복 체크
        if len(lecture_ids) != len(set(lecture_ids)):
            raise serializers.ValidationError("Duplicate lecture IDs are not allowed.")

        # 강의 유효성 검사
        invalid_ids = [id for id in lecture_ids if not Lecture.objects.filter(lecture_id=id).exists()]
        if invalid_ids:
            raise serializers.ValidationError(f"Invalid Lecture IDs: {invalid_ids}")

        # 관심 강의를 JSON 문자열로 변환
        #interests_json = json.dumps(lecture_ids)

        # 비밀번호 해싱
        validated_data['password'] = make_password(validated_data['password'])

        # User 생성
        user = User.objects.create(**validated_data)

        # 관심 강의 저장
        user.interests = lecture_ids
        user.save()

        return user