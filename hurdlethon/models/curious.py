# models.py

from django.db import models
from ..models.user import User
from ..models.question import Question

class Curious(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'question']  # 한 사용자는 하나의 질문에 대해 한 번만 공감할 수 있음
