from .scorers import DICT_SCORERS
from .serializable import SerializedScore, SerializedQuestion, SerializedSubmission

class GraderServer(object):
  def __init__(self, questions):
    self.questions_by_dict = {q.name: q for q in questions}
    for question in questions:
      self.validate(question)

  def validate(self, question):
    # TODO: check that answer matches type_str
    # TODO: right validate
    pass

  def grade(self, submission):
    try:
      question = self.questions_by_dict[submission.question_name]
    except KeyError:
      return SerializedScore(score=0., error_msg='Invalid question name {}'.format(submission.question_name))

    # TODO: use question.type_str to validate submission.submission

    scorer = DICT_SCORERS[question.scorer_name](**question.scorer_params)
    return scorer.score(submission.submission, question.test_cases[0]['answer'])


class SerializedGraderServer(GraderServer):
  def __init__(self, questions_ser):
    questions = [SerializedQuestion.loads(q) for q in questions_ser]
    super(SerializedGraderServer, self).__init__(questions)

  def grade(self, submission_ser):
    submission = SerializedSubmission.loads(submission_ser)
    score = super(SerializedGraderServer, self).grade(submission)
    return score.dumps()
