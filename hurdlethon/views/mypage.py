import json

from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from hurdlethon.models import Lecture
from hurdlethon.serializers.mypage import MypageUpdateSerializer
from hurdlethon.serializers.user import UserSerializer


class MypageView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        # PUT 요청에서는 MypageUpdateSerializer 사용
        if self.request.method == 'PUT':
            return MypageUpdateSerializer
        return UserSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        # 유효성 검사
        serializer.is_valid(raise_exception=True)

        # 사용자 업데이트
        user = serializer.save()

        # 관심 강의를 리스트 형태로 반환
        interests = user.interests if isinstance(user.interests, list) else []

        # 응답 구성
        return Response(
            {
                "message": "회원 정보 수정 성공",
                "username": user.username,
                "nickname": user.nickname,
                "major": user.major,
                "school_email": user.school_email,
                "student_number": user.student_number,
                "interests": interests,
            },
            status=status.HTTP_200_OK
        )