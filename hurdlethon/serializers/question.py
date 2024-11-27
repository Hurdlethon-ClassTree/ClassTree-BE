from rest_framework import serializers

from .answer import AnswerSerializer
from .user import UserCreateSerializer
from ..models import Lecture
from ..models.question import Question
from ..models.user import User
from ..models.lecture import Lecture

#[GET] /question/<int:pk>/로 접근 시 얻는 정보
class QuestionSerializer(serializers.ModelSerializer):
    lecture_name = serializers.CharField(source='lecture_id.lecture_name', read_only=True)
    answers=AnswerSerializer(many=True, read_only=True)
    author = serializers.SerializerMethodField() # 동적 필드 : nickname or anonymous
    professor = serializers.CharField(source='lecture_id.professor', read_only=True)

    class Meta:
        model = Question
        fields = [ #professor 추가함
            'question_id', 'lecture_id','lecture_name', 'professor',
            'title', 'content', 'curious_count','point', 'author',
            'created_at', 'modified_at', 'checked', 'answers']

    def get_author(self, obj):
        """
        익명 여부(anonymous)에 따라 작성자(author) 설정
        """
        if obj.anonymous:
            return "anonymous"
        return obj.nickname  # 익명이 아니면 닉네임 반환

    def get_answers(self, obj):
        answers=obj.answer_set.all()
        return AnswerSerializer(answers, many=True).data

    def update(self, instance, validated_data):
        instance.checked = validated_data.get('checked', instance.checked)
        return super().update(instance, validated_data)

#/question/으로 질문 생성 시 사용
class QuestionCreateSerializer(serializers.ModelSerializer):
    anonymous = serializers.BooleanField(write_only=True, required=False)  # 익명 여부
    class Meta:
        model = Question
        fields = ['title', 'content', 'point', 'lecture_id', 'anonymous']  # 생성 시 작성 가능한 필드만

    def validate_point(self, value):
        if value < 0:
            raise serializers.ValidationError("Point must be a positive integer.")
        return value

    def validate_lecture_id(self, value):
        if not Lecture.objects.filter(lecture_id=value.lecture_id).exists():
            raise serializers.ValidationError("Invalid lecture ID.")
        return value

#/question/<int:pk>/로 질문 수정 시 사용
# point 확인 필요 x, 익명 여부 처리 x, 질문작성자만 수정 가능하게
class QuestionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['content']  # 수정 시 변경 가능한 필드만

    def validate_content(self, value):
        """
        작성자만 질문의 내용을 수정할 수 있도록 제한.
        """
        question = self.instance  # 현재 수정하려는 질문
        user = self.context['request'].user
        if user.pk != question.user_id.pk:  # 현재 사용자가 작성자와 일치하지 않으면
            raise serializers.ValidationError("작성자만 질문 내용을 수정할 수 있습니다.")
        # 채택된 질문은 수정할 수 없도록
        if question.checked:
            raise serializers.ValidationError("채택된 질문은 수정할 수 없습니다.")

        return value

    def update(self, instance, validated_data):
        """
        content만 수정할 수 있도록.
        """
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance