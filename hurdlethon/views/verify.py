from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.email import EmailVerification
from ..models.user import User
from django.core.mail import send_mail
class VerifyVerificationCodeView(APIView):
    def post(self, request, *args, **kwargs):
        school_email = request.data.get("school_email")
        verification_code = request.data.get("verification_code")

        if not school_email or not verification_code:
            return Response({"message": "이메일과 인증번호를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        # 이미 유저가 존재하는 경우
        if User.objects.filter(school_email=school_email).exists():
            return Response({"message": "이미 가입된 이메일입니다."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            verification = EmailVerification.objects.get(school_email=school_email)
        except EmailVerification.DoesNotExist:
            return Response({"message": "등록된 인증 요청이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        # 인증번호 유효성 검증
        if not verification.is_valid():
            return Response({"message": "인증번호가 만료되었습니다. 새 인증번호를 요청해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        if verification.verification_code != verification_code:
            # print(verification.verification_code, type(verification.verification_code))
            # print(verification_code, type(verification_code))
            return Response({"message": "잘못된 인증번호입니다."}, status=status.HTTP_400_BAD_REQUEST)
        # 인증 성공 처리
        return Response({"message": "이메일 인증이 완료되었습니다."}, status=status.HTTP_200_OK)