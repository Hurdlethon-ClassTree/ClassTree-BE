from django.db import models
from .lecture import Lecture
from .user import User
from .question import Question

class Answer(models.Model):
    ANSWER_ID=models.AutoField(primary_key=True) #답변
    QUESTION_ID = models.ForeignKey(Question, on_delete=models.CASCADE)
    CONTENT=models.TextField()
    CREATED_AT=models.DateTimeField(auto_now_add=True)
    MODIFIED_AT=models.DateTimeField(auto_now=True)

    USER_ID=models.ForeignKey(User,on_delete=models.CASCADE)
    LECTURE_ID=models.ForeignKey(Lecture,on_delete=models.CASCADE)
    LIKE=models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Answer by {self.USER_ID.username} to {self.QUESTION_ID.TITLE}"