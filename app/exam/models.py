import uuid

from django.db import models

from question.models import Question, Alternative

from student.models import Student


class Exam(models.Model):
    name = models.CharField(max_length=100)
    questions = models.ManyToManyField(Question, through='ExamQuestion', related_name='questions')

    def __str__(self):  # pragma: no cover
        return self.name


class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()

    class Meta:
        unique_together = ('exam', 'number')
        ordering = ['number']

    def __str__(self):  # pragma: no cover
        return f'{self.question} - {self.exam}'

class Answer(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4)
    exam_question = models.ForeignKey(ExamQuestion, on_delete=models.CASCADE)
    alternative = models.ForeignKey(Alternative, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_created=True, auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['exam_question', 'student'], name='unique_question_by_student')
        ]