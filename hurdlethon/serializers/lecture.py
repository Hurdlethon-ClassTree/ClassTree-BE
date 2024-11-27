from rest_framework import serializers
from ..models.lecture import Lecture

class LectureSerializer(serializers.ModelSerializer):
    lecture_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Lecture
        fields = [
            'lecture_id','lecture_code', 'lecture_name',  'professor', 'lecture_day',
             'lecture_time', 'semester', 'year'
        ]

    @classmethod
    def filter_queryset(cls, request):
        queryset = Lecture.objects.all()
        lecture_name = request.query_params.get('lecture_name')
        semester = request.query_params.get('semester')
        professor = request.query_params.get('professor')

        # 필터 조건 적용
        if lecture_name:
            queryset = queryset.filter(lecture_name__icontains=lecture_name)  # 강의명 검색
        if semester:
            queryset = queryset.filter(semester=semester)  # 학기 필터
        if professor:
            queryset = queryset.filter(professor__icontains=professor)  # 교수 이름 검색

        return queryset
