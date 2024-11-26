from rest_framework import serializers
from ..models.answer import Answer
class CheckSerializer(serializers.Serializer):
    answer_id = serializers.IntegerField()

    def validate_answer_id(self, value):
        # answer_id에 대한 유효성 검사 로직 추가
        if not Answer.objects.filter(id=value).exists():
            raise serializers.ValidationError("답변이 존재하지 않습니다.")
        return value
