from rest_framework import serializers, status, generics, permissions
from rest_framework.response import Response
from ..models.answer import Answer
from ..models.question import Question
from ..serializers.answer import AnswerSerializer
from ..serializers.question import QuestionSerializer

class CheckView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuestionSerializer  # 직렬화기 추가

    def get_queryset(self):
        """
        질문 작성자만 해당 질문에 대한 답변을 채택할 수 있도록 필터링.
        """
        question_id = self.kwargs['question_id']
        return Question.objects.filter(id=question_id, user=self.request.user)

    def post(self, request, *args, **kwargs):
        """
        답변을 채택하고 질문 및 답변 상태를 업데이트하는 메서드.
        """
        question_id = self.kwargs['question_id']
        answer_id = request.data.get('answer_id')

        # question_id에 해당하는 질문이 있는지 확인
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response({"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND)

        # answer_id에 해당하는 답변이 있는지 확인
        try:
            answer = Answer.objects.get(id=answer_id, question=question)
        except Answer.DoesNotExist:
            return Response({"error": "Answer not found or does not belong to the question"}, status=status.HTTP_400_BAD_REQUEST)

        # 질문 작성자만 채택 가능
        if request.user != question.user:
            return Response({"error": "Only the question author can select an answer"}, status=status.HTTP_403_FORBIDDEN)

        # 이미 채택된 답변이 있는지 확인
        if question.checked:
            return Response({"error": "Answer already selected"}, status=status.HTTP_400_BAD_REQUEST)

        # 선택된 답변을 채택 상태로 업데이트
        answer.is_checked = True
        answer.save()

        # 질문에 채택 완료 상태 표시
        question.checked = True
        question.save()

        # 답변 작성자에게 포인트 지급
        answer_user = answer.user
        answer_user.total_point += question.point  # 질문에 설정된 포인트만큼 답변 작성자에게 추가
        answer_user.save()

        # 성공 메시지 반환
        return Response({"result": "success"}, status=status.HTTP_201_CREATED)