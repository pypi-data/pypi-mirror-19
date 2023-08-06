import math

from itertools import izip

# yes this is janky, but works in practice
MIN_FLOAT = .00000001

def nextafter(a, b):
  """Return the next floating-point value after x1 towards x2, element-wise."""
  return a + MIN_FLOAT if a < b else a - MIN_FLOAT

def array(arr):
  return Array(arr)

def sqrt(x):
  if isinstance(x, Array):
    return Array([math.sqrt(y) for y in x])
  else:
    return math.sqrt(x)

def square(x):
  if isinstance(x, Array):
    return Array([y*y for y in x])

def var(x):
  avg = float(sum(x)) / float(len(x))
  return sum((avg - v) ** 2 for v in x) / float(len(x))

class Array(object):

  def __init__(self, arr):
    self.arr = arr

  def __radd__(self, other):
    return self.arr + other

  def __add__(self, other):
    return Array([i + j for i, j in zip(self.arr, other)])

  def __sub__(self, other):
    return Array([i - j for i, j in zip(self.arr, other)])

  def __rsub__(self, other):
    return Array([j - i for i, j in zip(self.arr, other)])

  def __eq__(self, other):
    return Array([int(x == y) for x, y in zip(self.arr, other)])

  def __str__(self):
    return str(self.arr)

  def __repr__(self):
    return str(self.arr)

  def __len__(self):
    return len(self.arr)

  def sum(self):
    return sum(self.arr)

  def __iter__(self):
    self.current = 0
    return self

  def next(self):
    if self.current >= len(self.arr):
      self.current = 0
      raise StopIteration
    else:
     ret_val = self.arr[self.current]
     self.current += 1
     return ret_val

  @property
  def size(self):
    return len(self.arr)

  @property
  def shape(self):
    return (len(self.arr),)
