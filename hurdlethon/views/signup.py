from rest_framework import generics, mixins, status, serializers
from rest_framework.response import Response

from ..models import Lecture
from ..models.email import EmailVerification
from ..serializers.user import UserCreateSerializer
from ..models.user import User
import json


class SignupView(mixins.CreateModelMixin, generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserCreateSerializer
    queryset = User.objects.none()  # 빈 queryset 설정

    def post(self, request, *args, **kwargs):
        '''회원가입 처리'''
        serializer = self.get_serializer(data=request.data)

        school_email = request.data.get('school_email')
        # 이메일 인증 여부 확인
        try:
            verification = EmailVerification.objects.get(school_email=school_email)
        except EmailVerification.DoesNotExist:
            return Response({"message": "이메일 인증이 완료되지 않았습니다. 먼저 인증을 진행해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        if not verification.is_valid():
            return Response({"message": "인증번호가 만료되었습니다. 다시 인증을 요청해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        # 회원가입 진행
        serializer = UserCreateSerializer(data=request.data)

        if serializer.is_valid():
            user=serializer.save()
            user.total_point=100 # initial point
            user.save()

            # 이메일 인증이 완료되었다면 인증 정보 삭제 (선택적 처리)
            if school_email:
                verification.delete()
            return Response(
                {
                    "message":"회원가입 성공",
                    "user":serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #[GET] /signup 시 강의목록 반환
    def get(self, request, *args, **kwargs):
        # 강의 선택을 위한 강의 목록 반환
        lectures = Lecture.objects.values('lecture_id', 'lecture_name')  # 강의 ID와 이름만 가져오기
        return Response(
            {
                "Valid Lectures": list(lectures)
            },
            status=status.HTTP_200_OK
        )