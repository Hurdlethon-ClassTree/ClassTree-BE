from rest_framework import serializers
from ..models.answer import Answer

class AnswerSerializer(serializers.ModelSerializer):
    QUESTION_TITLE = serializers.CharField(source='QUESTION_ID.TITLE', read_only=True)
    ANSWER_ID = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Answer
        fields = ['ANSWER_ID', 'CONTENT', 'QUESTION_ID', 'QUESTION_TITLE', 'CREATED_AT', 'MODIFIED_AT']