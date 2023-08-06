import unittest
import random

from static_grader import gae_numpy as gae_np
import numpy as np

"""
Test that everything from numpy we've implemented functions
"""


class GAENumpyTest(unittest.TestCase):
  def setUp(self):
    self.int_list = [random.randint(0, 50) for _ in range(100)]
    self.float_list = [100 * random.random() for _ in range(100)]

    self.int_gae = gae_np.array(self.int_list)
    self.float_gae = gae_np.array(self.float_list)
    self.int_np = np.array(self.int_list)
    self.float_np = np.array(self.float_list)

  def tearDown(self):
    pass

  def test_array_init(self):
    int_arr = gae_np.array(self.int_list)
    float_arr = gae_np.array(self.float_list)
    self.assertEqual(int_arr, np.array(self.int_list))
    self.assertEqual(float_arr, np.array(self.float_list))

  def test_len(self):
    self.assertEqual(len(self.int_list), len(self.int_gae))
    self.assertEqual(len(self.int_np), len(self.int_gae))

  def test_size(self):
    self.assertEqual(self.int_np.size, self.int_gae.size)

  def test_sqrt(self):
    self.assertAlmostEqual(np.sqrt(self.float_np), gae_np.sqrt(self.float_gae))
    self.assertAlmostEqual(np.sqrt(self.int_np), gae_np.sqrt(self.int_gae))

  def test_var(self):
    self.assertAlmostEqual(np.var(self.float_np), gae_np.var(self.float_gae))
    self.assertAlmostEqual(np.var(self.int_np), gae_np.var(self.int_gae))

  def test_sum(self):
    self.assertAlmostEqual(self.int_np.sum(), self.int_gae.sum())
    self.assertAlmostEqual(self.float_np.sum(), self.float_gae.sum())

  def test_add(self):
    for g, n in zip(self.float_np + self.int_np, self.float_gae + self.int_gae):
      self.assertAlmostEqual(g, n)

  def test_subtract(self):
    for g, n in zip(self.float_np - self.int_np, self.float_gae - self.int_gae):
      self.assertAlmostEqual(g, n)
    for g, n in zip(self.int_np - self.float_np, self.int_gae - self.float_gae):
      self.assertAlmostEqual(g, n)

  def test_shape(self):
    self.assertEqual(self.float_np.shape, self.float_gae.shape)

  def test_equality(self):
    gae_eq = (self.float_gae == self.float_gae)
    np_eq = (self.float_np == self.float_np)
    for g, n in zip(gae_eq, np_eq):
      self.assertEqual(g, n)

if __name__ == '__main__':
  unittest.main()
