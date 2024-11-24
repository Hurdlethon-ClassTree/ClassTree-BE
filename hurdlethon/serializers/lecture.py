from rest_framework import serializers
from ..models.lecture import Lecture

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = [
            'lecture_id', 'professor', 'lecture_code', 'name',
            'lecture_day', 'lecture_time', 'semester', 'year'
        ]
