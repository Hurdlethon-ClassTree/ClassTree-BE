from django.db import models
from .lecture import Lecture
from .user import User

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)  # 질문 아이디
    lecture_id = models.ForeignKey(Lecture, on_delete=models.CASCADE)  # 교과목 ID
    title = models.CharField(max_length=50)  # 제목
    content = models.TextField()  # 질문 내용
    checked = models.BooleanField(default=False)  # 채택 여부
    point = models.PositiveIntegerField(default=0)  # 포인트
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 일자
    modified_at = models.DateTimeField(auto_now=True)  # 수정 일자
    curious = models.PositiveIntegerField(default=0)  # 궁금해요
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # 작성자


    def __str__(self):
        return f"{self.question_id}: {self.title}"
