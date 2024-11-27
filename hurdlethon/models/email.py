from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import now
import random

class EmailVerification(models.Model):
    school_email = models.EmailField(unique=True)
    verification_code = models.IntegerField()
    #verification_code = models.CharField(max_length=6)
    code_expiration = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return now() < self.created_at + timedelta(minutes=5)

    @classmethod
    def save_verification_code(cls, email):
        # 인증번호 생성 및 저장
        verification_code = random.randint(100000, 999999)
        expiration_time = timezone.now() + timedelta(minutes=5)
        obj, created = cls.objects.update_or_create(
            school_email=email,
            defaults={"verification_code": verification_code, "code_expiration": expiration_time}
        )
        return obj
