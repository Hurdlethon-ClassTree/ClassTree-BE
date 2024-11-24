from rest_framework import generics, permissions, status
from ..models import Question
from ..serializers.question import QuestionSerializer
from rest_framework.response import Response
from rest_framework import serializers

class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
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