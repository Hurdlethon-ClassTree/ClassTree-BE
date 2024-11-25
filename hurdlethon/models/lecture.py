from django.db import models

class Lecture(models.Model):
    lecture_id = models.AutoField(primary_key=True)  # 과목 ID
    professor = models.CharField(max_length=50)  # 교수
    lecture_code = models.CharField(unique=True, max_length=50)  # 강의 코드
    lecture_name = models.CharField(max_length=50)  # 강의명
    lecture_day = models.CharField(max_length=7, verbose_name="강의 요일", help_text="월~일 (7자리 이진수)")  # 강의 요일
    lecture_time = models.CharField(max_length=50)  # 강의 시간
    semester = models.CharField(max_length=1, default='1', verbose_name="학기")  # 학기
    year = models.CharField(max_length=4, default='2024', verbose_name="년도")  # 년도

    class Meta:
        db_table = 'lecture'
        verbose_name = "강의"
    def __str__(self):
        return f"{self.lecture_id}: {self.lecture_code} {self.lecture_name}"