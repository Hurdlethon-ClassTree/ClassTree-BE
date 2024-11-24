from rest_framework import serializers
from ..models.answer import Answer

class AnswerSerializer(serializers.ModelSerializer):
    question_title = serializers.CharField(source='question_id.title', read_only=True)
    answer_id = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Answer
        fields = [
            'answer_id', 'content', 'question_id', 
            'question_title', 'created_at', 'modified_at', 
            'user_id', 'lecture_id', 'like'
        ]
