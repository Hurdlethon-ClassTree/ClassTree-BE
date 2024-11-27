from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from ..models import Question
from ..serializers.question import QuestionSerializer
from rest_framework.permissions import IsAuthenticated 

class RecentQuestionsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    """
    접속시간 기준으로 가장 최근에 올라온 질문 10개를 반환하는 API 뷰.
    """
    serializer_class = QuestionSerializer

    def get_queryset(self):
        # 가장 최근에 올라온 10개 질문을 내림차순으로 가져오기
        return Question.objects.all().order_by('-created_at')[:10]

    def get(self, request, *args, **kwargs):
        """
        GET 요청으로 최근 질문 10개를 반환합니다.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)