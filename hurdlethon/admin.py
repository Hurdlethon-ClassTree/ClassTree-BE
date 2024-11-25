from django.contrib import admin
from .models.user import User
from .models.lecture import Lecture
from .models.question import Question
from .models.answer import Answer

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'user_id', 'username', 'nickname', 'school_email', 
        'student_number', 'major', 'created_at', 'total_point', 'interests'
    )
    list_editable = ('total_point',)  # 목록에서 포인트 바로 수정 가능
    search_fields = ('username', 'nickname')
    readonly_fields = ('user_id',)

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('lecture_id', 'lecture_name', 'lecture_day', 'lecture_time', 'professor', 'semester', 'year')
    search_fields = ('lecture_id', 'lecture_name', 'professor')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'question_id', 'lecture_id', 'title', 'point', 
        'checked', 'created_at', 'modified_at'
    )
    list_filter = ('lecture_id', 'user_id')
    search_fields = ('title', 'content')
    readonly_fields = ('question_id',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'answer_id', 'question_id', 'created_at', 'modified_at', 
        'user_id', 'like'
    )
    list_filter = ('created_at', 'modified_at', 'user_id')
    search_fields = ('content', 'question_id__title')
