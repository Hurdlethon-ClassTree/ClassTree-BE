from rest_framework import serializers
from .user import UserSerializer
from ..models.question import Question

class QuestionSerializer(serializers.ModelSerializer):
    lecture_name = serializers.CharField(source='lecture_id.lecture_name', read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Question
        fields = [
            'question_id', 'content', 'lecture_id',
            'lecture_name', 'created_at', 'modified_at', 'user', 'checked', 'curious', 'point'
        ]

    def update(self, instance, validated_data):
        instance.checked = validated_data.get('checked', instance.checked)
        return super().update(instance, validated_data)
