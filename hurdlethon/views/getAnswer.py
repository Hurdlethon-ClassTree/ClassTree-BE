from hurdlethon.models import Question, Answer
from hurdlethon.serializers.answer import AnswerSerializer
from rest_framework import generics, permissions

class GetMyAnswers(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AnswerSerializer

    def get_queryset(self):
        # 현재 로그인한 사용자의 nickname으로 필터링

        return Answer.objects.filter(user_id=self.request.user.user_id)