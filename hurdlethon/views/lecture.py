from rest_framework import generics, permissions, serializers, status
from django.db.models import Q
from rest_framework.response import Response

from .question import QuestionListCreateView
from ..models import Lecture
from ..models.answer import Answer
from ..models.question import Question
from ..serializers.answer import AnswerSerializer
from ..serializers.lecture import LectureSerializer
from ..serializers.question import QuestionUpdateSerializer, QuestionCreateSerializer, QuestionSerializer


class LectureListView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

#/lecture/1/ 을 통해 lecture에 있는 질문 조회
class LectureDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Lecture.objects.prefetch_related('questions').all()
    serializer_class = QuestionSerializer
    def get(self, request, pk):
        try:
            lecture = Lecture.objects.get(pk=pk)
        except Lecture.DoesNotExist:
            return Response({"detail": "Lecture not found."}, status=404)
        lecture_id = lecture.lecture_id
        questions = Question.objects.filter(lecture_id=lecture_id)
        question_serializer = self.get_serializer(questions, many=True)
        return Response(question_serializer.data)