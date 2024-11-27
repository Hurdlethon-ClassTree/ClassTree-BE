from rest_framework import generics, status
from rest_framework.response import Response
from ..models.question import Question
from ..serializers.question import QuestionSerializer

class NoanswerQuestionsListView(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        # 답변이 없는 질문만 필터링하여 최근 10개를 가져옴
        return Question.objects.filter(answers__isnull=True).order_by('-created_at')[:10]

    def list(self, request, *args, **kwargs):
        # 쿼리셋을 가져와서 serializer로 변환
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"no_answer_questions": serializer.data}, status=status.HTTP_200_OK)
