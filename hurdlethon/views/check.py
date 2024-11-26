from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models.answer import Answer
from ..models.question import Question
from ..serializers.check import CheckSerializer
from rest_framework.exceptions import PermissionDenied


class CheckView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CheckSerializer

    def post(self, request, *args, **kwargs):
        question_id = self.kwargs['question_id']
        answer_id = request.data.get('answer_id')

        # question_id와 answer_id 필드를 _id로 수정
        try:
            question = Question.objects.get(question_id=question_id)
        except Question.DoesNotExist:
            return Response({"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            answer = Answer.objects.get(answer_id=answer_id, question_id=question_id)  # 외래 키를 question_id로 수정
        except Answer.DoesNotExist:
            return Response({"error": "Answer not found or does not belong to the question"}, status=status.HTTP_400_BAD_REQUEST)

        # 채택자는 질문 작성자여야 한다는 조건 체크
        if request.user != question.user_id:  # user_id로 비교해야 함
            return Response({"error": "Only the question author can select an answer"}, status=status.HTTP_403_FORBIDDEN)
        # 질문자는 자신의 답변을 채택할 수 없음

        if request.user == answer.user_id:
            return Response({"error": "You cannot select your own answer"}, status=status.HTTP_400_BAD_REQUEST) 

        # 이미 채택된 답변이 있는지 확인
        if question.checked:
            return Response({"error": "Answer already selected"}, status=status.HTTP_400_BAD_REQUEST)

        # 선택된 답변을 채택 상태로 업데이트
        answer.is_checked = True
        answer.save()

        # 질문에 채택된 답변을 반영
        question.checked = True
        question.save()

        # 답변 작성자에게 포인트 지급
        answer_user = answer.user_id  # user_id로 접근
        answer_user.total_point += question.point  # 질문에 설정된 포인트만큼 답변 작성자에게 추가
        answer_user.save()

        return Response({"result": "success"}, status=status.HTTP_201_CREATED)
