from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models.like import Like
from ..models.answer import Answer
from rest_framework import permissions
from django.db.models import F

class LikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # URL 경로에서 answer_id 가져오기
        answer_id = self.kwargs['answer_id']

        try:
            answer = Answer.objects.get(pk=answer_id)
        except Answer.DoesNotExist:
            return Response({"error": "Answer not found"}, status=status.HTTP_404_NOT_FOUND)

        # 이미 좋아요를 누른 사용자 확인
        existing_like = Like.objects.filter(user=request.user, answer=answer).first()

        if existing_like:
            # 좋아요 취소 (이미 좋아요를 누른 경우)
            existing_like.delete()
            Answer.objects.filter(pk=answer_id).update(like_count=F('like_count') - 1)
            answer.refresh_from_db()  # 최신 데이터 가져오기

            return Response({
                "liked_count": answer.like_count,
                "boolean": False  # 좋아요 취소
            }, status=status.HTTP_200_OK)

        else:
            # 좋아요 추가 (좋아요를 누른 적이 없는 경우)
            Like.objects.create(user=request.user, answer=answer)
            Answer.objects.filter(pk=answer_id).update(like_count=F('like_count') + 1)
            answer.refresh_from_db()  # 최신 데이터 가져오기

            return Response({
                "liked_count": answer.like_count,
                "boolean": True  # 좋아요 추가
            }, status=status.HTTP_200_OK)
