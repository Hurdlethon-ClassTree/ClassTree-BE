from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.email import EmailVerification
from ..models.user import User
from django.core.mail import send_mail
class SendVerificationCodeView(APIView):
    def post(self, request, *args, **kwargs):
        school_email = request.data.get("school_email")
        if not school_email:
            return Response({"message": "학교 이메일을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        if not school_email.endswith('@sogang.ac.kr'):
            return Response({"message": "학교 이메일은 @sogang.ac.kr로 끝나야 합니다."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(school_email=school_email).exists():
            return Response({"message": "이미 해당 이메일로 가입된 계정이 존재합니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 이메일 인증번호 생성 및 저장
        verification = EmailVerification.save_verification_code(email=school_email)
        # 이메일 발송
        mail_subject = "학교 이메일 인증번호"
        message = f"회원가입을 위한 인증번호는 {verification.verification_code}입니다. 5분 내에 인증을 완료해주세요."
        send_mail(mail_subject, message, "from@example.com", [school_email])
        return Response({"message": "인증번호가 이메일로 발송되었습니다."}, status=status.HTTP_200_OK)