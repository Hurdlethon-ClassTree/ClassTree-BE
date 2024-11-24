from rest_framework import serializers
from ..models.question import Question
from ..models.user import User
from ..models.lecture import Lecture

class QuestionSerializer(serializers.ModelSerializer):
    anonymous = serializers.BooleanField(write_only=True, required=False)  # 익명 여부

    class Meta:
        model = Question
        fields = [
            'question_id', 'title', 'content', 'checked', 'point',
            'created_at', 'modified_at', 'curious', 'anonymous',
            'lecture_id'
        ]
        read_only_fields = ['question_id', 'created_at', 'modified_at', 'curious', 'checked']

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