from django.contrib import admin
from django.urls import path

from hurdlethon.views.lecture import LectureListView
from hurdlethon.views.question import QuestionListCreateView, QuestionDetailView
from hurdlethon.views.answer import AnswerListCreateView, AnswerDetailView
from hurdlethon.views.signup import SignupView
from hurdlethon.views.login import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/",LoginView.as_view()),
    path("signup/",SignupView.as_view()),
    path("lecture/",LectureListView.as_view()),
    path("lecture/<int:pk>/",LectureListView.as_view(), name='lecture_detail'),

    path("question/", QuestionListCreateView.as_view()),
path('question/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
path('answer/', AnswerListCreateView.as_view(), name='answer_list_create'),
    path('answer/<int:pk>/', AnswerDetailView.as_view(), name='answer_detail'),
]
