from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models.curious import Curious
from ..models.question import Question
from rest_framework import permissions
from django.db.models import F

class CuriousView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # URL 경로에서 question_id 가져오기
        question_id = self.kwargs['question_id']

        try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            return Response({"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND)

        # 이미 공감을 표시한 사용자 확인
        existing_curious = Curious.objects.filter(user=request.user, question=question).first()

        # F()객체 사용하여 무결성검사 통해 DB레벨에서 안전하게 연산
        if existing_curious:
            # 공감 취소 (이미 공감한 경우)
            existing_curious.delete()
            Question.objects.filter(pk=question_id).update(curious_count=F('curious_count') - 1)
            question.refresh_from_db()  # 최신 데이터 가져오기

            return Response({
                "curious_count": question.curious_count,
                "boolean": False  # 공감 취소
            }, status=status.HTTP_200_OK)

        else:
            # 공감 추가 (공감을 표시한 적이 없는 경우)
            Curious.objects.create(user=request.user, question=question)
            Question.objects.filter(pk=question_id).update(curious_count=F('curious_count') + 1)
            question.refresh_from_db()  # 최신 데이터 가져오기

            return Response({
                "curious_count": question.curious_count,
                "boolean": True  # 공감 추가
            }, status=status.HTTP_200_OK)
