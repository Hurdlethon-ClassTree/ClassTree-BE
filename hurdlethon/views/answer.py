from rest_framework import generics, permissions, serializers, status
from django.db.models import Q
from rest_framework.response import Response
from ..models.answer import Answer
from ..models.question import Question
from ..serializers.answer import AnswerSerializer, AnswerCreateSerializer, AnswerUpdateSerializer
from rest_framework.exceptions import PermissionDenied


class AnswerListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self): #url에서 전달된 question_id에 답변
        question_id = self.kwargs['question_id']
        try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            return Answer.objects.none()

        
        return Answer.objects.filter(question_id=question_id)

        # if search_query:
        #     queryset=queryset.filter(Q(TITLE__icontains=search_query)|
        #                              Q(CONTENT__icontains=search_query)|
        #                              Q(LECTURE_ID__icontains=search_query))
        #     return queryset
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AnswerCreateSerializer
        return AnswerSerializer

    def perform_create(self, serializer):
        question_id= self.kwargs['question_id']
        print("question_id : ", question_id)
        try:
            question=Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            raise serializers.ValidationError({"question_id": "Invalid question_id."})
        if question.checked:
            raise serializers.ValidationError("채택된 질문에는 답변을 추가할 수 없습니다.")

        serializer.save(user_id=self.request.user,
                        question_id=question,
                        lecture_id=question.lecture_id
                        )

class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        question_id = self.kwargs['question_id']
        return Answer.objects.filter(question_id=question_id)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AnswerUpdateSerializer
        return AnswerSerializer

    def perform_update(self, serializer): #작성자만 수정 가능
        answer = serializer.instance
        question = answer.question_id
        if question.checked:
            raise serializers.ValidationError("채택된 질문에 대한 답변은 수정할 수 없습니다.")
        

        serializer.save()

    def perform_destroy(self, instance):
        """
        작성자만 답변을 삭제할 수 있도록 제한.
        """
        user = self.request.user

        if instance.user_id.pk != user.pk:
            raise PermissionDenied("작성자만 답변을 삭제할 수 있습니다.")  # Permission denied if not the author
        instance.delete()