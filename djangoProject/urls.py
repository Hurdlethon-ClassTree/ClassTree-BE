from django.contrib import admin
from django.urls import path

from hurdlethon.views.favorite import GetMyFavorite
from hurdlethon.views.getAnswer import GetMyAnswers
from hurdlethon.views.getQuestion import GetMyQuestions
from hurdlethon.views.lecture import LectureListView, LectureDetailView
from hurdlethon.views.mypage import MypageView
from hurdlethon.views.question import QuestionListCreateView, QuestionDetailView
from hurdlethon.views.answer import AnswerListCreateView, AnswerDetailView
from hurdlethon.views.signup import SignupView
from hurdlethon.views.login import LoginView
from hurdlethon.views.logout import Logout_view

from hurdlethon.views.check import CheckView 
from hurdlethon.views.curious import CuriousView
from hurdlethon.views.like import LikeView
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    # login, signup
    path("login/",LoginView.as_view()),
    path("signup/",SignupView.as_view()),

    path("lecture/",LectureListView.as_view()),
    path("lecture/<int:pk>/",LectureDetailView.as_view(), name='lecture_detail'),

    path("question/", QuestionListCreateView.as_view()),
    path('question/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('question/<int:question_id>/answer/', AnswerListCreateView.as_view(), name='answer_list_create'),
    path('question/<int:question_id>/answer/<int:pk>/', AnswerDetailView.as_view(), name='answer_detail'),
    path('mypage/', MypageView.as_view(), name='mypage'),
    path('mypage/question/', GetMyQuestions.as_view(), name='question_list_view'),
    path('mypage/answer/', GetMyAnswers.as_view(), name='question_list_view'),
    path('favorite/', GetMyFavorite.as_view(), name='question_list_view'),

    path('question/<int:question_id>/checked/', CheckView.as_view(), name='check_view'), # 답변 채택 여부 확인
    path('question/<int:question_id>/curious/', CuriousView.as_view(), name='curious_view'), # 질문 궁금해요
    path('question/<int:question_id>/answer/<int:answer_id>/like/', LikeView.as_view(), name='like_view'), # 답변 좋아요

    path('logout/', Logout_view, name='logout'),  # 로그아웃 URL 추가

]
