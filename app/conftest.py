import pytest

from app.exam.services import AnswersService
from question.models import Question, Alternative
from question.utils import AlternativesChoices
from student.models import Student
from exam.models import Exam, ExamQuestion


@pytest.fixture
def base_client(setup_database, client):
    return client

@pytest.fixture(autouse=True)
def setup_database(transactional_db):
    pass

@pytest.fixture
def exam():
    exam = Exam(name='Exam on test case')
    exam.save()
    return exam


@pytest.fixture
def full_exam(exam):
    alternatives = []
    alternatives_data = [
        {'alternative': AlternativesChoices.A.value, 'content': 'Pulmões', 'is_correct': False},
        {'alternative': AlternativesChoices.B.value, 'content': 'Estômago', 'is_correct': False},
        {'alternative': AlternativesChoices.C.value, 'content': 'Coração', 'is_correct': True},
        {'alternative': AlternativesChoices.D.value, 'content': 'Fígado', 'is_correct': False}
    ]
    question = Question(
        content='Qual órgão é responsável por bombear o sangue?'
    )
    question.save()
    for alternative_data in alternatives_data:
        alternatives.append(Alternative(
            question=question,
            content=alternative_data['content'],
            option=alternative_data['alternative'],
            is_correct=alternative_data['is_correct']
        ))

    exam_question = ExamQuestion(
        exam=exam,
        question=question,
        number=1
    )

    Alternative.objects.bulk_create(alternatives)
    exam_question.save()

    return exam

@pytest.fixture
def student():
    student = Student(
        name='test student',
        email='test@case.com'
    )
    student.save()
    return student

@pytest.fixture
def answers(full_exam, student):
    answers_data = []
    for exam_question in full_exam.examquestion_set.all():
        answers_data.append({
            'question_number': exam_question.number,
            'alternative': exam_question.question.alternatives.first().option
        })

    AnswersService().save_answers(student_id=student.id, exam_id=full_exam.id, answers_data=answers_data)
    return {
        'student': student,
        'exam': full_exam
    }
