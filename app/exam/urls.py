from django.urls import include, path
from rest_framework import routers

from exam.views import ExamViewSet, AnswerViewSet

exam_router = routers.DefaultRouter()
exam_router.register(r'exams', ExamViewSet)

answer_router = routers.DefaultRouter()
answer_router.register(r'answers', AnswerViewSet)

exam_urls = [
    path('', include(exam_router.urls)),
    path('', include(answer_router.urls)),
]