from rest_framework import generics, permissions, serializers, status
from django.db.models import Q
from rest_framework.response import Response

from ..models import Lecture
from ..models.answer import Answer
from ..models.question import Question
from ..serializers.answer import AnswerSerializer
from ..serializers.lecture import LectureSerializer


class LectureListView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class LectureDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    permission_classes = [permissions.IsAuthenticated]