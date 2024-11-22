from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User, Lecture, Question, Answer


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'STUDENT_NUMBER', 'password']

    def save(self, **kwargs):
        hashed_password=make_password(self.validated_data['password'])
        return super().save(password=hashed_password, **kwargs)

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['LECTURE_ID', 'NAME', 'LECTURE_DAY', 'LECTURE_TIME']


class QuestionSerializer(serializers.ModelSerializer):
    LECTURE_NAME = serializers.CharField(source='QUESTION_ID.LECTURE_ID', read_only=True)
    USER_ID = UserSerializer(read_only=True)
    class Meta:
        model = Question
        fields = ['QUESTION_ID','USER_ID','TITLE', 'CONTENT', 'LECTURE_NAME', 'POINT', 'CREATED_AT', 'MODIFIED_AT']
        read_only_fields = ['QUESTION_ID', 'CHECKED', 'CREATED_AT', 'MODIFIED_AT']  # 읽기 전용 필드 설정

    def update(self, instance, validated_data):
        instance.CHECKED=validated_data.get('CHECKED', instance.CHECKED)
        return super().update(instance, validated_data)

class AnswerSerializer(serializers.ModelSerializer):
    QUESTION_TITLE = serializers.CharField(source='QUESTION_ID.TITLE', read_only=True)
    ANSWER_ID = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Answer
        fields = ['ANSWER_ID', 'CONTENT', 'QUESTION_ID', 'QUESTION_TITLE', 'CREATED_AT', 'MODIFIED_AT']

