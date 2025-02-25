from http import HTTPStatus


def test_should_list_exams(base_client):
    # GIVEN
    # WHEN
    response = base_client.get('/exams/')
    data = response.json()

    # THEN
    assert type(data.get('count')) == int
    assert type(data.get('results')) == list
    assert response.status_code == HTTPStatus.OK.value


def test_should_retrieve_exams(base_client, exam):
    # GIVEN
    # WHEN
    response = base_client.get(f'/exams/{exam.id}/')
    data = response.json()

    # THEN
    assert exam.name == data.get('name')


def test_should_retrieve_exams_student_history(base_client, answers):
    # GIVEN
    # WHEN
    response = base_client.get(f'/exams/{answers.get("exam").id}/student/{answers.get("student").id}/history/')
    response_data = response.json()

    # THEN
    assert response_data.get('exam') == answers.get('exam').id
    assert response_data.get('number_of_answers') == 1
    assert response_data.get('answers')[0].get('question_number') == 1
    assert response.status_code == HTTPStatus.OK.value


def test_should_not_retrieve_exams_student_history_due_invalid_student(base_client, answers):
    # GIVEN
    # WHEN
    response = base_client.get(f'/exams/{answers.get("exam").id}/student/{9999}/history/')
    response_data = response.json()

    # THEN
    assert response_data.get('error') == 'Student not found'
    assert response.status_code == HTTPStatus.BAD_REQUEST.value


def test_should_not_retrieve_exams_student_history_due_invalid_exam(base_client, answers):
    # GIVEN
    # WHEN
    response = base_client.get(f'/exams/{9999}/student/{answers.get("student").id}/history/')
    response_data = response.json()

    # THEN
    assert response_data.get('error') == 'Exam not found'
    assert response.status_code == HTTPStatus.BAD_REQUEST.value


def test_should_retrieve_exams_student_history_with_no_answers(base_client, exam, student):
    # GIVEN
    # WHEN
    response = base_client.get(f'/exams/{exam.id}/student/{student.id}/history/')
    response_data = response.json()

    # THEN
    assert response_data.get('answers') == []
    assert response.status_code == HTTPStatus.OK.value