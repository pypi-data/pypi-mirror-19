import unittest

from static_grader import scorers, serializable

class TestFlask(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_threshold_scorer(self):
    SUBMISSION=[("a", 1)]
    SOLUTION=[("a", 1)]
    scorer = scorers.DICT_SCORERS['ThresholdScorer']
    self.assertEqual(scorer().score(SUBMISSION, SOLUTION), serializable.SerializedScore(1.0, ''))

if __name__ == '__main__':
  unittest.main()
