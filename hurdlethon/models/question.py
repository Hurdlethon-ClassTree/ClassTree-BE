from django.db import models
from .lecture import Lecture
from .user import User

class Question(models.Model):
    QUESTION_ID=models.AutoField(primary_key=True) #질문 아이디
    LECTURE_ID=models.ForeignKey(Lecture,on_delete=models.CASCADE)#교과목 ID
    TITLE=models.CharField(max_length=50)
    CONTENT=models.TextField() #질문내용
    CHECKED=models.BooleanField(default=False) #채택 여부
    POINT=models.PositiveIntegerField(default=0) #포인트
    CREATED_AT=models.DateTimeField(auto_now_add=True)#생성일자
    MODIFIED_AT=models.DateTimeField(auto_now=True)
    CURIOUS = models.PositiveIntegerField(default=0) #궁금해요

    USER_ID=models.ForeignKey(User,on_delete=models.CASCADE) #작성자
    def __str__(self):
        return f"{self.QUESTION_ID}: {self.TITLE}"