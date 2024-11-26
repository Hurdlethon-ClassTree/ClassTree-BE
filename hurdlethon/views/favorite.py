from rest_framework.response import Response

from hurdlethon.models import Question
from hurdlethon.serializers.question import QuestionSerializer
from rest_framework import generics, permissions

class GetMyFavorite(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuestionSerializer

    def get_queryset(self):
        user=self.request.user
        interests = user.interests if user.interests else []
        return Question.objects.filter(lecture_id__in=interests, checked=False)