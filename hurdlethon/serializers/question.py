from rest_framework import serializers

from .answer import AnswerSerializer
from .user import UserCreateSerializer
from ..models import Lecture
from ..models.question import Question
from ..models.user import User
from ..models.lecture import Lecture

#[GET] /question/<int:pk>/로 접근 시 얻는 정보
class QuestionSerializer(serializers.ModelSerializer):
    lecture_name = serializers.CharField(source='lecture_id.name', read_only=True)
    user = UserCreateSerializer(read_only=True)
    answers=AnswerSerializer(many=True, read_only=True)
    anonymous = serializers.BooleanField(write_only=True, required=False)  # 익명 여부

    class Meta:
        model = Question
        fields = [ #answer도 추가함
            'title', 'content', 'lecture_id','point', 'nickname',
            'lecture_name', 'created_at', 'modified_at', 'user', 'checked', 'curious', 'answers', 'anonymous']

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
class QuestionUpdateSerializer(serializers.ModelSerializer):
    anonymous = serializers.BooleanField(write_only=True, required=False)  # 익명 여부
    class Meta:
        model = Question
        fields = ['content','anonymous']  # 수정 시 변경 가능한 필드만
    def validate_point(self, value):
        """
        작성자가 충분한 포인트를 가지고 있는지 확인.
        """
        user = self.context['request'].user
        if user.total_point < value:  # User 모델에서 보유 포인트 확인
            raise serializers.ValidationError("포인트가 부족합니다.")
        return value

    def create(self, validated_data):
        """
        질문 생성 시 익명 여부 처리 및 사용자 포인트 차감.
        """
        user = self.context['request'].user

        # 익명 여부 처리
        anonymous = validated_data.pop('anonymous', False)
        nickname = "익명" if anonymous else user.nickname

        # 질문 생성
        question = Question.objects.create(
            **validated_data
        )

        # 포인트 차감
        user.total_point -= validated_data['point']  # 수정된 total_point 사용
        user.save()

        return question
