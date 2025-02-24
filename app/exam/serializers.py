from rest_framework import serializers

from exam.models import Exam, Answers

from question.utils import AlternativesChoices


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'name', 'questions']


class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ['id', 'question', 'answer', 'student', 'created']


class AnswerResponse(serializers.BaseSerializer):
    number = serializers.IntegerField()
    alternative = serializers.ChoiceField(choices=AlternativesChoices)


class AnswersRequestSerializer(serializers.BaseSerializer):
    student = serializers.CharField(max_length=32)
    exam = serializers.CharField(max_length=32)
    answers = AnswerResponse(many=True)

