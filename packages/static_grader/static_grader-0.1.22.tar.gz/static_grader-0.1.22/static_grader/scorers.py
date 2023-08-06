"""
A static list of scorers are available through scorer_getter.
Scorers are specified in the static grader

To add a scorer, add to the list `_SCORERS`
"""

import os
import sys
import re
try:
  import ujson as json
except ImportError:
  import json

import numpy as np
import requests

from .serializable import SerializedScore


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
  def parse(cls, submission,  # pylint: disable=R0913
            normalize=True,
            key_indices=(0,),
            value_indices=(1,),
            unordered_key=False):

    # Handle JSON strings
    if isinstance(submission, basestring):
      return self.parse(json.loads(submission))

    if isinstance(submission, dict):
      result = submission
    elif key_indices is None: # list of values
      result = dict((i, val) for i, val in enumerate(submission))
    elif value_indices is None: # list of keys
      result = dict((s, 1) for s in submission)
    else:
      if len(key_indices) == 1:
        keys = [s[key_indices[0]] for s in submission]
        if isinstance(keys[0], list):
          keys = [tuple(k) for k in keys]
      else:
        keys = [tuple(s[i] for i in key_indices) for s in submission]

      if len(value_indices) == 1:
        values = [s[value_indices[0]] for s in submission]
      else:
        values = [tuple(s[i] for i in value_indices) for s in submission]

      result = dict(zip(keys, values))

    if normalize:
      result = {cls.normalize(k): v for k, v in result.iteritems()}

    if unordered_key:
      result = {tuple(sorted(k)): v for k, v in result.iteritems()}


    return result


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
      return s.lower()
    elif isinstance(s, str):
      return s.decode("utf-8", "replace").lower()
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



def get_scores_spark(test, truth):
  test_dict = dict(test)
  truth_dict = dict(truth)

  common_keys = set(test_dict.keys()).intersection(set(truth_dict.keys()))

  pred_threshold = 0.5

  for key in common_keys:
    test_dict[key] = [1.0 if prob >= pred_threshold else 0.0
                      for prob in test_dict[key]]

  #return [precision_score(truth_dict[key], test_dict[key])
  #        for key in sorted(common_keys)]
  return [0 for key in sorted(common_keys)]

class OneVsAllScorer(ListScorer):
  def score(self, theirs, truth): # pylint: disable=W0221
    threshold = self.__dict__.get('threshold', 0.05)
    our_score = self.__dict__.get('our_score', [-1] * 100)
    their_score = get_scores_spark(theirs, truth)
    scorer = self.pct_diff_threshold(threshold=threshold, scale=len(our_score))
    return SerializedScore(score=self.score_intersection(our_score, their_score, scorer, fuzzy=True), error_msg='')

class RMSEScorer(Scorer):
  def __init__(self, our_score=0.0):
    self.our_score = our_score

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
    their_rmse = self.metric(submission_preds, ground_truth)
    if their_rmse == 0:
      return SerializedScore(1.0, error_msg='')

    return SerializedScore(self.our_score / their_rmse, error_msg='')

class AccuracyScorer(Scorer):
  def __init__(self, our_score=0.0):
    self.our_score = our_score

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
    return SerializedScore(self.metric(submission_preds, ground_truth) / self.our_score, error_msg='')




class ThresholdScorer(ListScorer):
  def score(self, submission, answer):
    threshold = self.__dict__.get('threshold', 0.05)
    normalize_keys = self.__dict__.get('normalize_keys', True)
    key_indices = self.__dict__.get('key_indices', [0])
    value_indices = self.__dict__.get('value_indices', [1])
    unordered_key = self.__dict__.get('unordered_key', False)
    fuzzy = self.__dict__.get('fuzzy', False)

    output = self.parse(submission, key_indices=key_indices,
                        value_indices=value_indices, normalize=normalize_keys,
                        unordered_key=unordered_key)
    solution = self.parse(answer, key_indices=key_indices,
                          value_indices=value_indices, normalize=normalize_keys,
                          unordered_key=unordered_key)
    scorer = self.pct_diff_threshold(threshold=threshold, scale=len(submission))


    return SerializedScore(score=self.score_intersection(solution, output, scorer, fuzzy=fuzzy),
                           error_msg='')


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

class URLScorer(Scorer):

  def score(self, submission, _):
    regex = self.__dict__.get('url_regex', None)

    if regex and not re.compile(regex).match(submission):
      return SerializedScore(0., error_msg='')

    if requests.get(submission).status_code == 200:
      return SerializedScore(1., error_msg='')
    else:
      return SerializedScore(0., error_msg='')



LIST_SCORERS = [ExactIntScorer, ExactListScorer, RMSEScorer,
                RSquaredScorer, AccuracyScorer, ThresholdScorer, URLScorer]

DICT_SCORERS = dict((cl.__name__, cl) for cl in LIST_SCORERS)

