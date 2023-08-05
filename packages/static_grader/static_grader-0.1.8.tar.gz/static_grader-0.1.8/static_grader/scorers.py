"""
A static list of scorers are available through scorer_getter.
Scorers are specified in the static grader

To add a scorer, add to the list `_SCORERS`
"""

import os
import sys
import re

import numpy as np
import toolz
import requests
from sklearn.metrics import precision_score

from serializable import SerializedScore


class Scorer(object):
  def __init__(self, **scorer_params):
    """
    Provide key word arguments via scorer_params that can be accessed in `self.score`
    """
    self.__dict__.update(scorer_params)

  def score(self, submission, question):
    """
    Fill in a function that graders submissions that returns a Score object
    """
    raise NotImplemented

class ExactIntScorer(Scorer):
  def score(self, submission, answer):
    """
    for int only
    """
    score = int(int(submission) == int(answer))
    return SerializedScore(score=score, error_msg='')

class ExactListScorer(Scorer):
  def score(self, submission, answer):
    """
    for int only
    """
    score = str(submission) == answer
    return SerializedScore(score=score, error_msg='')

class ListScorer(Scorer):
  @classmethod
  def parse(cls, submission,
            normalize=True,
            key_indices=[0],
            value_indices=[1]):

    if key_indices == [0] and value_indices == [1]: # key, value dict
      if isinstance(submission, dict):
        dictized = submission
      elif isinstance(submission[0][0], list):
        dictized = dict((tuple(k), v) for k, v in submission)
      else:
        dictized = dict(submission)
    elif key_indices is None: # list of values
      dictized = dict((i, val) for i, val in enumerate(submission))
    elif value_indices is None: # list of keys
      dictized = dict((s, 1) for s in submission)
    else:
      keys = [tuple(item[index] for index in key_indices) for item in submission]
      values = [tuple(item[index] for index in value_indices) for item in submission]
      dictized = dict(zip(keys, values))

    if normalize:
      return {cls.normalize(k): v for k, v in dictized.iteritems()}
    else:
      return dictized



  @classmethod
  def normalize(cls, s):
    """ Normalizes `basestring`. Lowercases and converts to `utf-8`.

    Will also broadcast itself across tuples and lists.

    :param s: `str` or `unicode`, or `tuple` or `list`
    :returns: `unicode` (utf-8), or `tuple` of unicode
              or original value if not normalizable
    """
    if isinstance(s, (tuple, list)):
      return tuple(cls.normalize(string) for string in s)
    if isinstance(s, unicode):
      string = s.encode("utf-8", "replace")
      return string.decode("utf-8").lower()
    elif isinstance(s, str):
      return s.decode("utf-8").lower()
    else:
      return s

  @classmethod
  def pct_diff_threshold(cls, threshold=0.1, scale=100):
    def pct_diff_scorer(x, y):
      if y is None:
        return 0
      if isinstance(x, (list, tuple)):
        return float(sum(pct_diff_scorer(a, b) for a, b in zip(x, y))) / len(x)

      if cls.pct_diff(x, y) > threshold:
        return 0
      else:
        return 1.0 / scale
    return pct_diff_scorer

  @classmethod
  def pct_diff(cls, x, y):
      """ Returns the magnitude of the percent difference of `y` from `x`

      :param x: `float`
      :param y: `Optional[float]`
      :returns: `float` >= 0
      """

      if x is None or y is None:
          return float('inf')
      if x == 0:  # divide by 0 errors
          x = np.nextafter(0, 1)
      if y == 0:  # need to preserve equality if x = y
          y = np.nextafter(0, 1)
      return abs(x - y) / float(x)

  @classmethod
  def fuzzy_get(cls, key, options):
    """Get a fuzzy match of `key` in `options`. Returns `None` if no match
    found.

    Uses `difflib` under the hood.

    :param key: `T` (usually `str` or `Tuple[str]`).
    :param options: `Dict<T, float>`
    :returns: `Optional[float]`
    """
    import difflib

    cutoff = 0.85

    if isinstance(key, basestring):
      matches = difflib.get_close_matches(key, options, cutoff=cutoff, n=1)
      if matches:
        return options[matches[0]]
    elif isinstance(key, tuple):
      matcher = difflib.SequenceMatcher()
      max_score = 0
      max_key = None
      for option in options:
        s = 0
        for a, b in zip(key, option):
          matcher.set_seqs(a, b)
          s += matcher.ratio()

        if s > len(key) * cutoff and s > max_score:
          max_score = s
          max_key = option

      if max_key is not None:
        return options[max_key]

  @classmethod
  def score_intersection(cls, solution, submission, score_func, fuzzy=False):
    """ Scores the (possibly fuzzy) intersection between `solution` and
    `submission` using `score_func`.

    For each key in `solution`, compares the `solution` value with the
    corresponding `submission` value. Scores the two values, and then sums over
    all solution keys.

    :param solution: reference solution
    :type solution: dict[K, V]
    :param submission: fellow submission
    :type submission: dict[K, V]
    :param bool fuzzy: Whether to perform a fuzzy match. Defaults to `False`
    :param score_func: Scores two answers from a single key.
    :type score_func: function(V, Optional[V]) -> float
    :returns: 0 <= `float` <= 1
    """
    if fuzzy:
      get = cls.fuzzy_get
    else:
      get = lambda x, y: y.get(x, None)

    score = sum(score_func(value, get(name, submission))
                for name, value in solution.iteritems())
    return cls.clip(score)

  @classmethod
  def clip(cls, x):
    """ Ensures input is in [0, 1]

    :param number x:
    :returns: 0 <= float <= 1
    """
    return max(0.0, min(1.0, x))


class RMSEScorer(Scorer):
  @classmethod
  def metric(cls, theirs, truth):
    theirs = np.array(theirs)
    truth = np.array(truth)

    if theirs.size != truth.size:
      raise AssertionError("Wrong sizes")

    return np.sqrt(np.square(truth - theirs).sum() / float(truth.shape[0]))

  def score(self, submission_preds, ground_truth): # pylint: disable=W0221
    """Scorer for a machine learning question where the ground truth is known

    Score is the ratio of reference solution's root mean square error (rmse)
    and the fellow's rmse.

    :param submission_preds: their submitted predictions
    :param ground_truth: the true values being predicted
    """
    our_score = self.__dict__.get('our_score', 0.0)
    their_rmse = self.metric(submission_preds, ground_truth)
    if their_rmse == 0:
      return SerializedScore(1.0, error_msg='')

    return SerializedScore(our_score / their_rmse, error_msg='')

class RSquaredScorer(Scorer):
  @classmethod
  def metric(cls, theirs, truth):
    theirs = np.array(theirs)
    truth = np.array(truth)
    if theirs.size != truth.size:
      raise AssertionError("Wrong sizes")

    var = np.var(truth)
    mse = np.square(truth - theirs).sum() / float(truth.shape[0])
    return 1 - mse / var

  def score(self, submission_preds, ground_truth): # pylint: disable=W0221
    our_score = self.__dict__.get('our_score', 0.0)
    their_score = self.metric(submission_preds, ground_truth)
    return SerializedScore(their_score / our_score, error_msg='')

class AccuracyScorer(Scorer):
  @classmethod
  def metric(cls, theirs, truth):
    if isinstance(theirs, dict):
      theirs = [theirs[k] for k in sorted(theirs)]
    if isinstance(truth, dict):
      truth = [truth[k] for k in sorted(truth)]
    theirs = np.array(theirs)
    truth = np.array(truth)

    return float((theirs == truth).sum()) / len(truth)

  def score(self, submission_preds, ground_truth): # pylint: disable=W0221
    our_score = self.__dict__.get('our_score', 0.0)
    return SerializedScore(self.metric(submission_preds, ground_truth) / our_score, error_msg='')

def get_scores_spark(test, truth):
  test_dict = dict(test)
  truth_dict = dict(truth)

  common_keys = set(test_dict.keys()).intersection(set(truth_dict.keys()))

  pred_threshold = 0.5

  for key in common_keys:
    test_dict[key] = [1.0 if prob >= pred_threshold else 0.0
                      for prob in test_dict[key]
                      if test_dict[key] != truth_dict[key]]

  return [precision_score(truth_dict[key], test_dict[key])
          for key in sorted(common_keys)]

class OneVsAllScorer(ListScorer):
  def score(self, theirs, truth):
    threshold = self.__dict__.get('threshold', 0.05)
    our_score = self.__dict__.get('our_score', [-1] * 100)
    their_score = get_scores_spark(theirs, truth)
    scorer = self.pct_diff_threshold(threshold=threshold, scale=len(our_score))
    their_score_dict = self.parse(their_score, key_indices=None)
    our_score_dict = self.parse(our_score, key_indices=None)
    return SerializedScore(score=self.score_intersection(our_score_dict, their_score_dict, scorer, fuzzy=True), error_msg='')


class ThresholdScorer(ListScorer):
  def score(self, submission, answer):
    threshold = self.__dict__.get('threshold', 0.05)
    normalize_keys = self.__dict__.get('normalize_keys', True)
    key_indices = self.__dict__.get('key_indices', [0])
    value_indices = self.__dict__.get('value_indices', [1])

    output = self.parse(submission, key_indices=key_indices,
                        value_indices=value_indices, normalize=normalize_keys)
    solution = self.parse(answer, key_indices=key_indices,
                          value_indices=value_indices, normalize=normalize_keys)
    scorer = self.pct_diff_threshold(threshold=threshold, scale=len(submission))



    return SerializedScore(score=self.score_intersection(solution, output, scorer), error_msg='')


class URLScorer(Scorer):

  def score(self, submission, _):
    regex = self.__dict__.get('url_regex', None)

    if regex and not re.compile(regex).match(submission):
      return SerializedScore(0., error_msg='')

    if requests.get(submission).status_code == 200:
      return SerializedScore(1., error_msg='')
    else:
      return SerializedScore(0., error_msg='')


DICT_SCORERS = [ExactIntScorer, ExactListScorer, RMSEScorer,
                RSquaredScorer, AccuracyScorer, ThresholdScorer, URLScorer]
