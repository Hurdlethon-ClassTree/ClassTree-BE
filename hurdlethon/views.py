from django.db.migrations import serializer
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate, login

from .models import Question, Answer
from .serializers import LoginSerializer, UserSerializer, LectureSerializer, QuestionSerializer, AnswerSerializer
from rest_framework import mixins, generics, serializers, status, permissions
from django.db.models import Q

class LoginView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        if not user:
            raise AuthenticationFailed("아이디 또는 비밀번호가 틀렸습니다")

        login(request, user)

        return Response({"message": "로그인 성공", "user": {"username": user.username, "student_number": user.STUDENT_NUMBER}})

class SignupView(mixins.CreateModelMixin, generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            return Response(
                {
                    "message":"회원가입 성공",
                    "user":{
                        "student_number": user.STUDENT_NUMBER,
                        "id": user.id,
                    },
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(USER_ID=self.request.user)

class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
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