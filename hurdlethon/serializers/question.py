from rest_framework import serializers
from .user import UserSerializer
from ..models import Lecture
from ..models.question import Question

#/question/<int:pk>/로 get요청 시 보내는 정보
class QuestionSerializer(serializers.ModelSerializer):
    lecture_name = serializers.CharField(source='lecture_id.name', read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Question
        fields = [ #answer도 추가해야함
            'title', 'content', 'lecture_id',
            'lecture_name', 'created_at', 'modified_at', 'user', 'checked', 'curious'
        ]

    def update(self, instance, validated_data):
        instance.checked = validated_data.get('checked', instance.checked)
        return super().update(instance, validated_data)

#/question/으로 질문 생성 시 사용
class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['title', 'content', 'point', 'lecture_id']  # 생성 시 작성 가능한 필드만

    def validate_point(self, value):
        if value < 0:
            raise serializers.ValidationError("Point must be a positive integer.")
        return value

    def validate_lecture_id(self, value):
        if not Lecture.objects.filter(lecture_id=value.lecture_id).exists():
            raise serializers.ValidationError("Invalid lecture ID.")
        return value

#/question/<int:pk>/로 질문 수정 시 사용
class QuestionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['content']  # 수정 시 변경 가능한 필드만
