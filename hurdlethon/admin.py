from django.contrib import admin

# Register your models here.
# from django.contrib import admin
# from .models import Lecture, Question, Answer

# @admin.register(Lecture)
# class LectureAdmin(admin.ModelAdmin):
#     list_display = ('LECTURE_ID', 'NAME', 'LECTURE_DAY', 'LECTURE_TIME')
#     search_fields = ('LECTURE_ID', 'NAME')

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ('QUESTION_ID', 'LECTURE_ID', 'TITLE', 'POINT', 'CHECKED', 'CREATED_AT', 'MODIFIED_AT')
#     list_filter = ('LECTURE_ID','USER_ID')
#     search_fields = ('TITLE', 'CONTENT')
#     readonly_fields = ('QUESTION_ID',)

# @admin.register(Answer)
# class AnswerAdmin(admin.ModelAdmin):
#     list_display = ( 'QUESTION_ID', 'CREATED_AT', 'MODIFIED_AT')
#     list_filter = ('CREATED_AT', 'MODIFIED_AT')
#     search_fields = ('QUESTION_ID', 'CONTENT')


