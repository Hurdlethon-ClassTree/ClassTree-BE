from django.db import models

class Lecture(models.Model):
    lecture_id = models.AutoField(primary_key=True)  # 과목 ID
    professor = models.CharField(max_length=50)  # 교수
    lecture_code = models.CharField(unique=True, max_length=50)  # 강의 코드
    name = models.CharField(max_length=50)  # 강의명
    lecture_day = models.CharField(max_length=50)  # 강의 요일
    lecture_time = models.CharField(max_length=50)  # 강의 시간
    semester = models.CharField(max_length=50, default='1')  # 학기
    year = models.CharField(max_length=50, default='2024')  # 년도

    def __str__(self):
        return f"{self.lecture_id}: {self.lecture_code} {self.name}"