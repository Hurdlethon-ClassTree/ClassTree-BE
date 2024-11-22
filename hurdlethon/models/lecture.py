from django.db import models

class Lecture(models.Model):
    LECTURE_ID=models.AutoField(primary_key=True)#과목 id
    PROFESSOR=models.CharField(max_length=50)#교수
    LECTURE_CODE=models.CharField(unique=True, max_length=50)
    NAME=models.CharField(max_length=50)
    LECTURE_DAY=models.CharField(max_length=50)
    LECTURE_TIME=models.CharField(max_length=50)
    #lecture 학기, 년도
    SEMESTER=models.CharField(max_length=50, default='1')
    YEAR=models.CharField(max_length=50, default='2024')
    def __str__(self):
        return f"{self.LECTURE_ID}: {self.LECTURE_CODE} {self.NAME}"