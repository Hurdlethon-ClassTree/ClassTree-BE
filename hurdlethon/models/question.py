from django.db import models
from .lecture import Lecture
from .user import User

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)  # 질문 아이디
    title = models.CharField(max_length=50)  # 제목
    content = models.TextField()  # 질문 내용
    checked = models.BooleanField(default=False)  # 채택 여부
    point = models.PositiveIntegerField(default=0)  # 포인트
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 일자
    modified_at = models.DateTimeField(auto_now=True)  # 수정 일자
    
    curious_count = models.PositiveIntegerField(default=0)  # 궁금해요
    nickname = models.CharField(max_length=50, null=True, blank=True)  # 질문 작성자의 닉네임 
    anonymous = models.BooleanField(default=False)  # 익명 여부

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # 작성자
    lecture_id = models.ForeignKey(Lecture, on_delete=models.CASCADE, verbose_name="강의", related_name="questions")  # 교과목 ID
    def __str__(self):
        return f"{self.question_id}: {self.title}"
