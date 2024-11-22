from rest_framework import generics, permissions, serializers, status
from django.db.models import Q
from rest_framework.response import Response
from ..models.answer import Answer
from ..models.question import Question
from ..serializers.answer import AnswerSerializer
class AnswerListCreateView(generics.ListCreateAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        search_query=self.request.query_params.get('search', '')
        queryset=Answer.objects.all()

        if search_query:
            queryset=queryset.filter(Q(TITLE__icontains=search_query)|
                                     Q(CONTENT__icontains=search_query)|
                                     Q(LECTURE_ID__icontains=search_query))
            return queryset

    def perform_create(self, serializer):
        question_id=self.request.data.get('QUESTION_ID')
        try:
            question=Question.objects.get(QUESTION_ID=question_id)
        except Question.DoesNotExist:
            raise serializers.ValidationError({"QUESTION_ID": "Invalid QUESTION_ID."})

        serializer.save(USER_ID=self.request.user,
                        QUESTION_ID=question)


class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Answer.objects.filter(USER_ID=self.request.user)

    def perform_update(self, serializer): #작성자만 수정 가능
        if serializer.instance.USER_ID != self.request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()