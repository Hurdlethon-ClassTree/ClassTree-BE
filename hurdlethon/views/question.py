from rest_framework import generics, permissions, status
from ..models import Question
from ..serializers.question import QuestionCreateSerializer, QuestionUpdateSerializer, QuestionSerializer
from rest_framework.response import Response
from rest_framework import serializers

class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        특정 강의의 질문만 필터링하거나 전체 질문 반환.
        """
        lecture_id = self.request.query_params.get('lecture_id')
        if lecture_id:
            return Question.objects.filter(lecture_id=lecture_id)
        return super().get_queryset()
    def perform_create(self, serializer):
        """
        질문 작성 로직: 작성자(user_id), 닉네임(nickname), 익명 여부 처리.
        """
        user = self.request.user

        # 포인트 유효성 검사
        point = serializer.validated_data.get('point', 0)
        if user.total_point < point:
            raise serializers.ValidationError("포인트가 부족합니다.")

        # 질문 저장
        serializer.save(user_id=user)

        # 포인트 차감
        user.total_point -= point
        user.save()

    def create(self, request, *args, **kwargs):
        """
        POST 요청 처리: 성공/실패 응답.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"result": "success"}, status=status.HTTP_201_CREATED, headers=headers)    
    

class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.select_related("lecture_id","user_id").prefetch_related("answers__user_id")
    #queryset = Question.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    #serializer_class = QuestionSerializer

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
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return queryset.filter(user_id=self.request.user)
        #get 요청일 때는 모든 질문 볼 수 있음
        return queryset

    def perform_update(self, serializer):
        serializer.save(user_id=self.request.user)