from tabnanny import verbose

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    STUDENT_NUMBER=models.CharField(max_length=8, verbose_name="학번")
    class Meta:
        db_table='user'
        verbose_name="유저"

class Lecture(models.Model):
    LECTURE_ID=models.CharField(max_length=10) #과목 id
    NAME=models.CharField(max_length=50)
    LECTURE_DAY=models.CharField(max_length=50)
    LECTURE_TIME=models.CharField(max_length=50)

    def __str__(self):
        return self.LECTURE_ID

class Question(models.Model):
    QUESTION_ID=models.AutoField(primary_key=True) #질문 아이디
    LECTURE_ID=models.ForeignKey(Lecture,on_delete=models.CASCADE)#교과목 ID
    TITLE=models.CharField(max_length=50)
    CONTENT=models.TextField() #질문내용
    CHECKED=models.BooleanField(default=False) #채택 여부
    POINT=models.PositiveIntegerField(default=0) #포인트
    CREATED_AT=models.DateTimeField(auto_now_add=True)#생성일자
    MODIFIED_AT=models.DateTimeField(auto_now=True)

    USER_ID=models.ForeignKey(User,on_delete=models.CASCADE) #작성자
    def __str__(self):
        return f"{self.QUESTION_ID}: {self.TITLE}"

class Answer(models.Model):
    #ANSWER_ID=models.CharField(max_length=50)
    QUESTION_ID = models.ForeignKey(Question, on_delete=models.CASCADE)
    CONTENT=models.TextField()
    CREATED_AT=models.DateTimeField(auto_now_add=True)
    MODIFIED_AT=models.DateTimeField(auto_now=True)

    USER_ID=models.ForeignKey(User,on_delete=models.CASCADE)
    #LECTURE_ID=models.ForeignKey(Lecture,on_delete=models.CASCADE)

    def __str__(self):
        return f"Answer by {self.USER_ID.username} to {self.QUESTION_ID.TITLE}"


