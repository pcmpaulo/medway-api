from http import HTTPStatus, HTTPMethod

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from exam.models import Exam, Answer
from exam.serializers import AnswerSerializer, ExamSerializer, CreateAnswersSerializer, AnswerHistorySerializer

from exam.services import AnswersService

from student.models import Student


class ExamViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    queryset = Exam.objects.all().order_by('-id')
    serializer_class = ExamSerializer

    @action(detail=True, methods=[HTTPMethod.GET], url_path='student/(?P<student_id>[^/.]+)/history')
    def student_detail(self, request, *args, **kwargs):
        try:
            student = Student.objects.get(id=kwargs.get('student_id'))
            exam = Exam.objects.get(id=kwargs.get('pk'))

            answers_history_serializer = AnswerHistorySerializer(
                data=list(Answer.objects.filter(exam_question__exam=exam, student=student).distinct()),
                many=True
            )
            answers_history_serializer.is_valid()
            answers = answers_history_serializer.data

            history = {
                'exam': exam.id,
                'student': student.id,
                'correct_answers': sum([1 if answer.get('is_correct') else 0 for answer in answers]),
                'number_of_answers': len(answers),
                'accuracy_rate': 0,
                'answers': answers
            }
            if history.get('number_of_answers') > 0:
                history.update({'accuracy_rate': history.get('correct_answers') / history.get('number_of_answers')})

            return Response(history, status=HTTPStatus.OK.value)
        except ObjectDoesNotExist as error:
            if 'Student' in str(error):
                return Response({'error': 'Student not found'}, status=HTTPStatus.BAD_REQUEST.value)
            elif 'Exam' in str(error):
                return Response({'error': 'Exam not found'}, status=HTTPStatus.BAD_REQUEST.value)


class AnswerViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Answer.objects.all().order_by('-created')
    serializer_class = AnswerSerializer

    def create(self, request, *args, **kwargs):
        try:
            if not request.data.get('answers'):
                return Response({'error': 'Need to have at least one Answer'}, status=HTTPStatus.BAD_REQUEST.value)

            answers_serializer = CreateAnswersSerializer(data=request.data.get('answers'), many=True)
            answers_serializer.is_valid(raise_exception=True)

            answers = AnswersService().save_answers(
                student_id=request.data.get('student'),
                exam_id=request.data.get('exam'),
                answers_data=answers_serializer.validated_data
            )

            return Response(AnswerSerializer(answers, many=True).data, status=HTTPStatus.CREATED.value)
        except ObjectDoesNotExist as error:
            if 'Student' in str(error):
                return Response({'error': 'Student not found'}, status=HTTPStatus.BAD_REQUEST.value)
            elif 'ExamQuestion' in str(error):
                return Response({'error': 'Exam Question not found'}, status=HTTPStatus.BAD_REQUEST.value)
            elif 'Exam' in str(error):
                return Response({'error': 'Exam not found'}, status=HTTPStatus.BAD_REQUEST.value)
        except ValidationError as error:
            return Response({'error': error.detail}, status=HTTPStatus.BAD_REQUEST.value)