from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class CppQuestion(models.Model):
    # user info
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # creation date
    question_creation_date = models.DateTimeField(auto_now_add=True)

    # valid or not
    is_valid = models.BooleanField(default=False, help_text="Verify this question's validity")

    # question type
    THEORY = 'TH'
    PRACTICE = 'PR'
    QUESTION_TYPES = [
        (THEORY, 'theory'),
        (PRACTICE, 'practice')
    ]
    question_type = models.CharField(
        max_length=2,
        choices=QUESTION_TYPES,
        default=PRACTICE
    )

    # question level
    HARD = 'H'
    MEDIUM = 'M'
    EASY = 'E'
    QUESTION_LEVELS = [
        (HARD, 'hard'),
        (MEDIUM, 'medium'),
        (EASY, 'easy')
    ]
    question_level = models.CharField(
        max_length=1,
        choices=QUESTION_LEVELS,
        default=EASY
    )

    # question content
    question_content = models.TextField(
        max_length=1000,
        help_text="Enter your question content."
    )
    # question answer
    question_answer = models.TextField(
        max_length=1000,
        help_text="Enter your question answer."
    )

    def __str__(self):
        return self.question_content[:50]

class CppQuestionBase(models.Model):
    # user info
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # creation date
    question_creation_date = models.DateTimeField(auto_now_add=True)

    # valid or not
    is_valid = models.BooleanField(default=False, help_text="Verify this question's validity")

    # question content
    question_content = models.TextField(
        max_length=1000,
        help_text="Enter your question content."
    )
    # question answer
    question_answer = models.TextField(
        max_length=1000,
        help_text="Enter your question answer."
    )

    def __str__(self):
        return self.question_content[:50]


class EasyTheoryCppQuestion(CppQuestionBase):
    POINT = 10

class MediumTheoryCppQuestion(CppQuestionBase):
    POINT = 10
class HardTheoryCppQuestion(CppQuestionBase):
    POINT = 10

class EasyPracticeCppQuestion(CppQuestionBase):
    POINT = 10

class MediumPracticeCppQuestion(CppQuestionBase):
    POINT = 10
class HardPracticeCppQuestion(CppQuestionBase):
    POINT = 10