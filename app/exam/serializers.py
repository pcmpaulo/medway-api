from rest_framework import serializers

from exam.models import Exam, Answer

from question.utils import AlternativesChoices


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'name', 'questions']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'exam_question', 'alternative', 'student', 'created']

class CreateAnswersSerializer(serializers.Serializer):
    question_number = serializers.IntegerField(required=True)
    alternative = serializers.ChoiceField(choices=AlternativesChoices)