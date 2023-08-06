'''
Serializable classes that can be passed via RPC

Note: we must use setattr rather than class inheritance to add methods.
Class inheritance seems to erase the __dict__ method which is set in namedtuple
'''

from collections import namedtuple
import json

def serializable_namedtuple(*args, **kwargs):
  """
  A json serializable object with fields _fields
  """
  cls = namedtuple(*args, **kwargs)

  def dumps(self):
    return json.dumps({f: self.__getattribute__(f) for f in self._fields})
  setattr(cls, 'dumps', dumps)

  def loads(cls, string):
    js = json.loads(string)
    return cls(**{k: js[k] for k in cls._fields})
  setattr(cls, 'loads', classmethod(loads))

  return cls

# The question class needs to be serializable so that we can store questions in a DB
SerializedQuestion = serializable_namedtuple('Question', [
  'name',         # a string unique identifier for the question
  'scorer_name',  # the name of hte scorer to use
  'scorer_params', # a json object passed to the scorer object (see scorer)
  'test_cases'
])

# Student submission
SerializedSubmission = serializable_namedtuple('Submission', [
  'question_name',  # a stirng specifying the question name
  'submission'      # a possibly blank string.
])

# Score or erro returned by submission
SerializedScore = serializable_namedtuple('Score', [
  'score',      # a number between 0.1 and 1.0
  'error_msg'   # a possibly blank string.
])
