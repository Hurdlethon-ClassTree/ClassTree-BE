from rest_framework import generics, permissions, serializers, status
from rest_framework.generics import ListAPIView
from django.db.models import Q
from rest_framework.response import Response

from ..models import Lecture
from ..models.question import Question
from ..serializers.lecture import LectureSerializer
from ..serializers.question import QuestionSerializer
from rest_framework.exceptions import NotFound

class LectureListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    def get_queryset(self):
        queryset = Lecture.objects.all()
        lecture_name = self.request.query_params.get('lecture_name')
        semester = self.request.query_params.get('semester')
        professor = self.request.query_params.get('professor')
        semester = self.request.query_params.get('semester') 

        if lecture_name:
            queryset = queryset.filter(lecture_name__icontains=lecture_name)  # 강의명 검색
        if semester:
            queryset = queryset.filter(semester=semester)  # 학기 필터
        if professor:
            queryset = queryset.filter(professor__icontains=professor)  # 교수 이름 검색
        if semester:
            queryset = queryset.filter(semester=semester)
        return queryset
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"lecture_list": serializer.data})

class LectureDetailView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Lecture.objects.prefetch_related('questions').all()
    serializer_class = QuestionSerializer
    def get_queryset(self):
        lecture_id = self.kwargs.get('pk')  # URL에서 강의 ID 가져오기
        try:
            lecture = Lecture.objects.prefetch_related('questions').get(pk=lecture_id)
        except Lecture.DoesNotExist:
            raise NotFound("Lecture not found.")
                # 기본 쿼리셋
        
        queryset = lecture.questions.all()

        # 쿼리 파라미터 처리
        checked = self.request.query_params.get('checked')
        curious_min = self.request.query_params.get('curious_min')
        point_min = self.request.query_params.get('point_min')
        sort_by = self.request.query_params.get('sort_by')
        # print(f"Checked parameter value: {checked}")  # 로그 추가
        # 필터링 적용
        if checked is not None:
            checked_value = checked.strip().lower() == 'true'  # 문자열 'true' -> True 변환
            queryset = queryset.filter(checked=checked_value)
        if curious_min is not None:
            queryset = queryset.filter(curious__gte=int(curious_min))  # 궁금해요 최소값 필터링
        if point_min is not None:
            queryset = queryset.filter(point__gte=int(point_min))  # 포인트 최소값 필터링

        # 정렬 적용
        if sort_by:
            queryset = queryset.order_by(sort_by)
        
        return queryset  # 강의와 연결된 질문 반환
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "lecture_id": self.kwargs.get('pk'),
            "questions": serializer.data
        })