from tabnanny import verbose

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    USER_ID = models.BigAutoField(primary_key=True, verbose_name="사용자 ID")  # 기본 키

    USERNAME = models.CharField(max_length=50, unique=True, verbose_name="로그인용 ID")  # 로그인용 ID    
    NICKNAME = models.CharField(max_length=50, verbose_name="닉네임")  # 닉네임
    EMAIL = models.EmailField(max_length=50, unique=True, verbose_name="이메일")  # 이메일
    SCHOOL_EMAIL = models.EmailField(max_length=50, verbose_name="학교 이메일", null=True, blank=True)  # 학교 이메일

    PASSWORD = models.CharField(max_length=128, verbose_name="비밀번호")  # 비밀번호
    STUDENT_NUMBER = models.CharField(max_length=8, verbose_name="학번", null=True, blank=True)  # 학번
    MAJOR = models.CharField(max_length=50, verbose_name="전공", null=True, blank=True)  # 전공

    CREATED_AT = models.DateTimeField(auto_now_add=True, verbose_name="생성 일자")  # 생성 일자
    TOTAL_POINT = models.BigIntegerField(default=0, verbose_name="점수 총점")  # 점수 총점
    INTERESTS = models.TextField(verbose_name="관심 있는 과목", null=True, blank=True)  # 관심 있는 과목
    
    class Meta:
        db_table='user'
        verbose_name="유저"