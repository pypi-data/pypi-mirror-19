import unittest
import json

from grader_server import GraderServer, SerializedGraderServer
from serializable import SerializedQuestion, SerializedSubmission, SerializedScore

TEST_CASES = [
  {"args": ["abcd",  0.2], "kwargs": {}, "answer": 2}
]

class TestServer(unittest.TestCase):
  def test_grader_server(self):
    grade_server = GraderServer([SerializedQuestion('one_plus_one', 'int', 'ExactScorer', {}, TEST_CASES)])

    score = grade_server.grade(SerializedSubmission(question_name='one_plus_one', submission=2))
    assert score.score == 1.0
    assert score.error_msg == ''

    score = grade_server.grade(SerializedSubmission(question_name='one_plus_one', submission=0))
    assert score.score == 0.0
    assert score.error_msg == ''

    score = grade_server.grade(SerializedSubmission(question_name='no_question', submission=0))
    assert score.score == 0.0
    assert score.error_msg.startswith("Invalid")

  def test_serialized_grader_server(self):
    q_ser = SerializedQuestion('one_plus_one', 'int', 'ExactScorer', {}, TEST_CASES).dumps()
    grade_server = SerializedGraderServer([q_ser])

    score = SerializedScore.loads(grade_server.grade(SerializedSubmission(question_name='one_plus_one', submission=2).dumps()))
    assert score.score == 1.0
    assert score.error_msg == ''

    score = SerializedScore.loads(grade_server.grade(SerializedSubmission(question_name='one_plus_one', submission=0).dumps()))
    assert score.score == 0.0
    assert score.error_msg == ''

    score = SerializedScore.loads(grade_server.grade(SerializedSubmission(question_name='no_question', submission=0).dumps()))
    assert score.score == 0.0
    assert score.error_msg.startswith("Invalid")


if __name__ == '__main__':
  unittest.main()
