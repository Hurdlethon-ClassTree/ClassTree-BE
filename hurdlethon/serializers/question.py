from rest_framework import serializers
from .user import UserSerializer
from ..models.question import Question

class QuestionSerializer(serializers.ModelSerializer):
    LECTURE_NAME = serializers.CharField(source='QUESTION_ID.LECTURE_ID', read_only=True)
    USER_ID = UserSerializer(read_only=True)
    class Meta:
        model = Question
        fields = ['QUESTION_ID', 'CONTENT', 'LECTURE_ID', 
                 'LECTURE_NAME', 'CREATED_AT', 'MODIFIED_AT', 'USER_ID', 'CHECKED']
    def update(self, instance, validated_data):
        instance.CHECKED=validated_data.get('CHECKED', instance.CHECKED)
        return super().update(instance, validated_data)