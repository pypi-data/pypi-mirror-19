"""
A static list of scorers are available through scorer_getter.
Scorers are specified in the static grader

To add a scorer, add to the list `_SCORERS`
"""

from serializable import SerializedScore

class Scorer(object):
  def __init__(self, **scorer_params):
    """
    Provide key word arguements via scorer_params that can be accessed in `self.score`
    """
    self.__dict__.update(scorer_params)

  def score(self, submission, answer):
    """
    Fill in a function that graders submissions that returns a Score object
    """
    raise NotImplemented

class ExactScorer(Scorer):
  def score(self, submission, answer):
    score = submission == answer
    return SerializedScore(score=score, error_msg='')

_SCORERS = (ExactScorer,)

SCORERS_DICT = {s.__name__: s for s in _SCORERS}
