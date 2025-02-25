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


class AnswerHistorySerializer(AnswerSerializer):
    is_correct = serializers.SerializerMethodField()
    question_number = serializers.SerializerMethodField()
    selected_option = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = ['is_correct', 'question_number', 'selected_option']

    def get_is_correct(self, model_object):
        return model_object.alternative.is_correct

    def get_question_number(self, model_object):
        return model_object.exam_question.number

    def get_selected_option(self, model_object):
        return model_object.alternative.option


class CreateAnswersSerializer(serializers.Serializer):
    question_number = serializers.IntegerField(required=True)
    alternative = serializers.ChoiceField(choices=AlternativesChoices)