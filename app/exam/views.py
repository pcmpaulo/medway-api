from http import HTTPStatus

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from exam.models import Exam, Answer
from exam.serializers import AnswerSerializer, ExamSerializer, CreateAnswersSerializer

from exam.services import AnswersService


class ExamViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    queryset = Exam.objects.all().order_by('-id')
    serializer_class = ExamSerializer


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
            elif 'Exam' in str(error):
                return Response({'error': 'Exam not found'}, status=HTTPStatus.BAD_REQUEST.value)
        except ValidationError as error:
            return Response({'error': error.detail}, status=HTTPStatus.BAD_REQUEST.value)