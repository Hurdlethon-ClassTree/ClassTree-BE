from tabnanny import verbose
import json
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    user_id = models.AutoField(primary_key=True, verbose_name="고유 아이디")  # 기본 키
    username = models.CharField(max_length=50, unique=True, verbose_name="아이디")  # 아이디
    nickname = models.CharField(max_length=50, verbose_name="닉네임")  # 닉네임
    school_email = models.EmailField(max_length=50, verbose_name="학교 이메일", null=True, blank=True)  # 학교 이메일
    student_number = models.CharField(max_length=8, verbose_name="학번", null=True, blank=True)  # 학번
    major = models.CharField(max_length=50, verbose_name="전공", null=True, blank=True)  # 전공
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 일자")  # 생성 일자
    total_point = models.PositiveIntegerField(default=0, verbose_name="점수 총점")  # 점수 총점
    # verification_code = models.IntegerField(null=True, blank=True)
    # expiration_time = models.DateTimeField(null=True, blank=True)
    # verified = models.BooleanField(default=False)

    interests = models.JSONField(default=list, verbose_name="관심 있는 과목", blank=True)  # 관심 있는 과목

    class Meta:
        db_table = 'user'
        verbose_name = "유저"

    def set_interests(self, interests_list):
        """리스트를 JSON 문자열로 변환하여 저장"""
        # self.interests = json.dumps(interests_list)
        self.interests = interests_list
        return self.interests

    def get_interests(self):
        """JSON 문자열을 리스트로 변환하여 반환"""
        # if isinstance(self.interests, str):
        #     return json.loads(self.interests)
        return self.interests