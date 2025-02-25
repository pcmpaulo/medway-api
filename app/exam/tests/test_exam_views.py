from http import HTTPStatus

from exam.models import Exam


def test_should_list_exams(base_client):
    # GIVEN

    # WHEN
    response = base_client.get('/exams/')
    data = response.json()

    # THEN
    assert type(data.get('count')) == int
    assert type(data.get('results')) == list
    assert response.status_code == HTTPStatus.OK.value


def test_should_retrieve_exams(base_client):
    # GIVEN
    exam = Exam(name='Test case exam')
    exam.save()

    # WHEN
    response = base_client.get(f'/exams/{exam.id}/')
    data = response.json()

    # THEN
    assert exam.name == data.get('name')