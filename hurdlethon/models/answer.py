from django.db import models
from .question import Question
from .user import User

class Answer(models.Model):
    #ANSWER_ID=models.CharField(max_length=50)
    QUESTION_ID = models.ForeignKey(Question, on_delete=models.CASCADE)
    CONTENT=models.TextField()
    CREATED_AT=models.DateTimeField(auto_now_add=True)
    MODIFIED_AT=models.DateTimeField(auto_now=True)

    USER_ID=models.ForeignKey(User,on_delete=models.CASCADE)
    #LECTURE_ID=models.ForeignKey(Lecture,on_delete=models.CASCADE)

    def __str__(self):
        return f"Answer by {self.USER_ID.username} to {self.QUESTION_ID.TITLE}"