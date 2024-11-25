from rest_framework import generics, permissions, serializers, status
from rest_framework.generics import ListAPIView
from django.db.models import Q
from rest_framework.response import Response

from .question import QuestionListCreateView
from ..models import Lecture
from ..models.question import Question
from ..serializers.lecture import LectureSerializer
from ..serializers.question import QuestionSerializer

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

class LectureDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Lecture.objects.prefetch_related('questions').all()
    serializer_class = QuestionSerializer
    def get_queryset(self):
        lecture_id = self.kwargs.get('pk')  # URL에서 강의 ID 가져오기
        try:
            lecture = Lecture.objects.prefetch_related('questions').get(pk=lecture_id)
        except Lecture.DoesNotExist:
            return Response({"detail": "Lecture not found."}, status=404)
        lecture_id = lecture.LECTURE_ID
        questions = Question.objects.filter(LECTURE_ID=lecture_id)
        question_serializer = self.get_serializer(questions, many=True)
        return Response(question_serializer.data)