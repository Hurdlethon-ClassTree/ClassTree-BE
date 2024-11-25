from rest_framework import generics, permissions, status
from ..models import Question, Lecture
from ..serializers.question import QuestionCreateSerializer, QuestionUpdateSerializer, QuestionSerializer
from rest_framework.response import Response
from rest_framework import serializers

class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    # 생성 시 title, content, point 설정
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QuestionCreateSerializer
        return QuestionSerializer
    #이거 왜 지우셨어요 코드가 안돌아가버리잔아요


    def get_serializer_context(self):
        """
        강의 개수를 동적으로 확인해 선택 가능한 개수 제한.
        """
        max_lectures = 10
        lecture_count = Lecture.objects.count()  # 강의 개수 확인
        return {"max_lectures": min(lecture_count, max_lectures)}

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
        serializer.save(user_id=self.request.user)

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