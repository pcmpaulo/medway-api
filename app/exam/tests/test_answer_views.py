import pytest
from http import HTTPStatus


def test_should_list_answers(base_client):
    # GIVEN

    # WHEN
    response = base_client.get('/answers/')
    data = response.json()

    # THEN
    assert type(data.get('count')) == int
    assert type(data.get('results')) == list
    assert response.status_code == HTTPStatus.OK.value

def test_should_create_answers(base_client, student, create_full_exam):
    # GIVEN
    request_data = {
        'student': student.id,
        'exam': create_full_exam.id,
        'answers': []
    }

    for exam_question in create_full_exam.examquestion_set.all():
        request_data['answers'].append({
            'question_number': exam_question.number,
            'alternative': exam_question.question.alternatives.first().option
        })

    # WHEN
    response = base_client.post('/answers/', data=request_data, content_type='application/json')
    response_data = response.json()

    # THEN
    assert len(response_data) == len(request_data['answers'])
    assert response.status_code == HTTPStatus.CREATED.value


def test_should_not_create_answers_due_invalid_student(base_client, create_full_exam):
    # GIVEN
    request_data = {
        'student': 9999,
        'exam': create_full_exam.id,
        'answers': []
    }

    for exam_question in create_full_exam.examquestion_set.all():
        request_data['answers'].append({
            'question_number': exam_question.number,
            'alternative': exam_question.question.alternatives.first().option
        })

    # WHEN
    response = base_client.post('/answers/', data=request_data, content_type='application/json')
    response_data = response.json()

    # THEN
    assert response_data.get('error') == 'Student not found'
    assert response.status_code == HTTPStatus.BAD_REQUEST.value

def test_should_not_create_answers_due_invalid_exam(base_client, student, create_full_exam):
    # GIVEN
    request_data = {
        'student': student.id,
        'exam': 9999,
        'answers': []
    }

    for exam_question in create_full_exam.examquestion_set.all():
        request_data['answers'].append({
            'question_number': exam_question.number,
            'alternative': exam_question.question.alternatives.first().option
        })

    # WHEN
    response = base_client.post('/answers/', data=request_data, content_type='application/json')
    response_data = response.json()

    # THEN
    assert response_data.get('error') == 'Exam not found'
    assert response.status_code == HTTPStatus.BAD_REQUEST.value

def test_should_not_create_answers_due_no_answers(base_client, student, create_full_exam):
    # GIVEN
    request_data = {
        'student': student.id,
        'exam': create_full_exam.id,
        'answers': []
    }

    # WHEN
    response = base_client.post('/answers/', data=request_data, content_type='application/json')
    response_data = response.json()

    # THEN
    assert response_data.get('error') == 'Need to have at least one Answer'
    assert response.status_code == HTTPStatus.BAD_REQUEST.value

def test_should_not_create_answers_due_invalid_answers(base_client, student, create_full_exam):
    # GIVEN
    request_data = {
        'student': student.id,
        'exam': create_full_exam.id,
        'answers': []
    }

    for exam_question in create_full_exam.examquestion_set.all():
        request_data['answers'].append({
            'alternative': exam_question.question.alternatives.first().option
        })

    # WHEN
    response = base_client.post('/answers/', data=request_data, content_type='application/json')
    response_data = response.json()

    # THEN
    assert 'This field is required.' in response_data.get('error')[0].get('question_number')
    assert response.status_code == HTTPStatus.BAD_REQUEST.value