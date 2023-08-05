import unittest
import json

from flask import Flask, request
from grader_server import SerializedGraderServer
from serializable import SerializedQuestion, SerializedSubmission, SerializedScore

TEST_CASES = [
  {"args": ["abcd",  0.2], "kwargs": {}, "answer": 2}
]

class TestFlask(unittest.TestCase):
  SUBMISSION_KEY = 'submission'

  def setUp(self):
    app = Flask(__name__)
    q_ser = SerializedQuestion('one_plus_one', 'int', 'ExactScorer', {}, TEST_CASES).dumps()
    grade_server = SerializedGraderServer([q_ser])

    @app.route('/', methods=['POST'])
    def grading():
      return grade_server.grade(request.form[self.SUBMISSION_KEY])

    self.app = app.test_client()

  def submit(self, submission):
    resp = self.app.post('/', data={self.SUBMISSION_KEY: submission.dumps()})
    assert resp.status_code == 200
    return SerializedScore.loads(resp.data)

  def test_flask(self):
    score = self.submit(SerializedSubmission(question_name='one_plus_one', submission=2))
    assert score.score == 1.0
    assert score.error_msg == ''

    score = self.submit(SerializedSubmission(question_name='one_plus_one', submission=0))
    assert score.score == 0.0
    assert score.error_msg == ''

    score = self.submit(SerializedSubmission(question_name='no_question', submission=0))
    assert score.score == 0.0
    assert score.error_msg.startswith('Invalid')


if __name__ == '__main__':
  unittest.main()

