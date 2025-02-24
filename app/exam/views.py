from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, mixins

from exam.models import Exam, Answers
from exam.serializers import ExamSerializer, AnswersSerializer

from exam.serializers import AnswersRequestSerializer


class ExamViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    queryset = Exam.objects.all().order_by('-id')
    serializer_class = ExamSerializer


class AnswersViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Answers.objects.all().order_by('-created')
    serializer_class = AnswersSerializer

    @swagger_auto_schema(request_body=AnswersRequestSerializer)
    def create(self, request, *args, **kwargs):
        return
