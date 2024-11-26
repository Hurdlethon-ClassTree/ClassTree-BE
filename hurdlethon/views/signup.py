# from rest_framework import  status
# from rest_framework.response import Response

# from ..models import Lecture
# from ..serializers.user import UserCreateSerializer
# from ..models.user import User
# from django.core.mail import send_mail
# from django.conf import settings
# from rest_framework.status import HTTP_400_BAD_REQUEST
# from django.utils import timezone
# from rest_framework.views import APIView
# # from datetime import timedelta
# import random


# class SignupView(APIView):
#     authentication_classes = []
#     permission_classes = []
#     serializer_class = UserCreateSerializer

#     def get_serializer_context(self):
#         """
#         강의 개수를 동적으로 확인해 선택 가능한 개수 제한.
#         """
#         lectures = Lecture.objects.all()
#         return {"lectures": lectures}


#     def post(self, request, *args, **kwargs):
#         school_email = request.data.get('school_email')
#         try:
#             user = User.objects.get(school_email=school_email, verified=True)
#         except User.DoesNotExist:
#             # user.delete()
#             return Response({"message": "이메일 인증이 완료되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)

#         # 인증번호 확인 후, 회원가입 진행

#         serializer = UserCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             user=serializer.save()
#             user.total_point=100 # initial point
#             user.save()

#             return Response(
#                 {
#                     "message":"회원가입 성공",
#                     "username": user.username,
#                     "initial_points": user.total_point,
#                     # "interests": json.loads(user.interests),
#                     "interests": user.interests,

#                 },
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     #[GET] /signup 시 강의목록 반환
#     def get(self, request, *args, **kwargs):
#         # 강의 선택을 위한 강의 목록 반환
#         lectures = Lecture.objects.values('lecture_id', 'lecture_name')  # 강의 ID와 이름만 가져오기
#         return Response(
#             {
#                 "Valid Lectures": list(lectures)
#             },
#             status=status.HTTP_200_OK
#         )
from rest_framework import mixins, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Lecture
from ..serializers.user import UserCreateSerializer
from ..models.user import User
from ..models.email import EmailVerification


class SignupView(mixins.CreateModelMixin, generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserCreateSerializer
    # queryset = User.objects.all()
    queryset = User.objects.none()  # 빈 queryset 설정
    def get_serializer_context(self):
        """
        강의 데이터를 동적으로 확인하여 선택 가능한 데이터 제공.
        """
        lectures = Lecture.objects.values('lecture_id', 'lecture_name')
        return {"lectures": lectures}

    def post(self, request, *args, **kwargs):
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
            user = serializer.save()
            user.total_point = 100  # 초기 포인트 설정
            user.save()

            # 인증 성공 후, EmailVerification 삭제 (선택)
            verification.delete()

            return Response(
                {
                    "message": "회원가입이 완료되었습니다.",
                    "username": user.username,
                    "initial_points": user.total_point,
                    "interests": user.interests,
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        """
        강의 목록 반환
        """
        lectures = Lecture.objects.values('lecture_id', 'lecture_name')  # 강의 ID와 이름만 가져오기
        if not lectures.exists():
            return Response({"message": "등록된 강의가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {"Valid Lectures": list(lectures)},
            status=status.HTTP_200_OK
        )
