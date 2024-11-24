from rest_framework import generics, permissions, status
from ..models import Question
from ..serializers.question import QuestionCreateSerializer, QuestionUpdateSerializer, QuestionSerializer
from rest_framework.response import Response

class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]

    #생성 시 title, content, point 설정
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QuestionCreateSerializer
        return QuestionCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.select_related("lecture_id","user_id",).all()

    permission_classes = [permissions.IsAuthenticated]

    #QuesitonUpdateSerializer
    #수정 시 content 설정
    def get_serializer_class(self):
        #get 요청 시 질문 내용 볼 수 있음
        if self.request.method in ['GET']:
            return QuestionSerializer
        #수정 시 가능한 필드
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return QuestionUpdateSerializer
        return QuestionUpdateSerializer

    def get_queryset(self):
        queryset=super().get_queryset()
        if self.request.method in ['PUT', 'PATCH']:
            return queryset.filter(user_id=self.request.user)
        #get 요청일 때는 모든 질문 볼 수 있음
        return queryset

    def perform_update(self, serializer):
        serializer.save(user_id=self.request.user)