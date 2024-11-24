from rest_framework import generics, permissions, status
from ..models import Question
from ..serializers.question import QuestionSerializer
from rest_framework.response import Response

class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(USER_ID=self.request.user)
        
class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.select_related("answer").all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    #질문내용 수정
    def get_queryset(self):
        queryset=super().get_queryset()
        if self.request.method == 'GET':
            return queryset
        return queryset.filter(USER_ID=self.request.user)

    #채택완료 표시
    def perform_update(self, serializer):
        if serializer.instance.USER_ID != self.request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if 'CHECKED' in serializer.validated_data and not serializer.instance.CHECKED:
            serializer.save(CHECKED=True)
        return serializer.save()