from rest_framework import serializers
from ..models.lecture import Lecture

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['LECTURE_ID', 'PROFESSOR', 'LECTURE_CODE', 'NAME', 'LECTURE_DAY', 'LECTURE_TIME', 'SEMESTER', 'YEAR'] 