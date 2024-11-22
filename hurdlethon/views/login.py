from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import generics
from ..serializers.login import LoginSerializer

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