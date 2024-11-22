from django.db import models

class Lecture(models.Model):
    LECTURE_ID=models.CharField(max_length=10) #과목 id
    NAME=models.CharField(max_length=50)
    LECTURE_DAY=models.CharField(max_length=50)
    LECTURE_TIME=models.CharField(max_length=50)

    def __str__(self):
        return self.LECTURE_ID