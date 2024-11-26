from django.db import models
from .lecture import Lecture
from .user import User
from .question import Question

class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)  # 답변 ID
    question_id = models.ForeignKey(Question,
                                    on_delete=models.CASCADE,
                                    related_name="answers")  # 질문 ID

    content = models.TextField()  # 답변 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 일자
    modified_at = models.DateTimeField(auto_now=True)  # 수정 일자

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # 작성자

    lecture_id = models.ForeignKey(Lecture, on_delete=models.CASCADE)  # 강의 ID
    
    like_count = models.PositiveIntegerField(default=0)  # 좋아요 수

    is_checked = models.BooleanField(default=False)  # 채택 여부를 표시하는 필드

    def __str__(self):
        return f"Answer by {self.user_id.username} to {self.question_id.title}"
