from rest_framework import serializers
from ..models.answer import Answer

#[GET] /answer/<pk>/로 접근 시 얻는 정보
class AnswerSerializer(serializers.ModelSerializer):
    question_title = serializers.CharField(source='question_id.title', read_only=True)
    answer_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Answer
        fields = [
            'question_id','question_title',
            'answer_id', 'content',
             'created_at', 'modified_at',
            'user_id', 'lecture_id', 'like'
        ]

class AnswerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['content']
        read_only_fields = ['user_id', 'question_id', 'lecture_id']


class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['content']
        read_only_fields = ['user_id', 'question_id', 'lecture_id']
