from rest_framework.response import Response

from hurdlethon.models import Question
from hurdlethon.serializers.question import QuestionSerializer
from rest_framework import generics, permissions

class GetMyQuestions(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuestionSerializer

    def get_queryset(self):
        # 현재 로그인한 사용자의 nickname으로 필터링
        return Question.objects.filter(nickname=self.request.user.nickname)