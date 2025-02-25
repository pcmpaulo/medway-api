from student.models import Student
from exam.models import Exam, Answer, ExamQuestion
from question.models import Alternative

from question.utils import AlternativesChoices


class AnswersService:

    @staticmethod
    def _get_student(student_id):
        return Student.objects.get(id=student_id)

    @staticmethod
    def _get_exam(exam_id):
        return Exam.objects.get(id=exam_id)

    def save_answers(self, student_id: int, exam_id: int, answers_data: list):
        answers = []
        student = self._get_student(student_id)
        exam = self._get_exam(exam_id)
        for answer_data in answers_data:
            exam_question = self._get_exam_question(exam, answer_data.get('question_number'))
            alternative = self._get_alternative(exam_question, answer_data.get('alternative'))

            answers.append(Answer(
                exam_question=exam_question,
                alternative=alternative,
                student=student
            ))

        return Answer.objects.bulk_create(
            answers, update_conflicts=True, unique_fields=['exam_question', 'student'], update_fields=['alternative']
        )

    @staticmethod
    def _get_exam_question(exam: Exam, question_number: int) -> ExamQuestion:
        return exam.examquestion_set.get(number=question_number)

    @staticmethod
    def _get_alternative(exam_question: ExamQuestion, alternative: AlternativesChoices) -> Alternative:
        return exam_question.question.alternatives.get(option=alternative)