from rest_framework import serializers
from ..models.answer import Answer

#[GET] /answer/<pk>/로 접근 시 얻는 정보
class AnswerSerializer(serializers.ModelSerializer):
    question_title = serializers.CharField(source='question_id.title', read_only=True)
    answer_id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(source='user_id.username', read_only=True)  # 추가된 부분

    
    class Meta:
        model = Answer
        fields = [
            'question_id','question_title',
            'answer_id', 'content',
            'created_at', 'modified_at',
            'user_id', 'lecture_id', 'like_count', 'is_checked', 'username'
        ]

class AnswerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['content']
        read_only_fields = ['user_id', 'question_id', 'lecture_id']

    def validate_content(self, value):
        """
        작성자만 질문의 내용을 수정할 수 있도록 제한.
        """
        answer = self.instance  # 현재 수정하려는 질문
        user = self.context['request'].user
        if user.pk != answer.user_id.pk:  # 현재 사용자가 작성자와 일치하지 않으면
            raise serializers.ValidationError("작성자만 질문 내용을 수정할 수 있습니다.")
        return value

    def update(self, instance, validated_data):
        """
        content만 수정할 수 있도록.
        """
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance


class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['content']
        read_only_fields = ['user_id', 'question_id', 'lecture_id']
