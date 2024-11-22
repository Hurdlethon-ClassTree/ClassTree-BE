from django.db import models

class Lecture(models.Model):
    LECTURE_ID=models.AutoField(primary_key=True)#과목 id
    PROFESSOR=models.CharField(max_length=50)#교수
    LECTURE_CODE=models.CharField(max_length=50)
    NAME=models.CharField(max_length=50)
    LECTURE_DAY=models.CharField(max_length=50)
    LECTURE_TIME=models.CharField(max_length=50)
    def __str__(self):
        return self.LECTURE_ID