from rest_framework import serializers
from ..models.lecture import Lecture

class LectureSerializer(serializers.ModelSerializer):
    lecture_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Lecture
        fields = [
            'lecture_id', 'professor', 'lecture_code', 'lecture_name',
            'lecture_day', 'lecture_time', 'semester', 'year'
        ]
