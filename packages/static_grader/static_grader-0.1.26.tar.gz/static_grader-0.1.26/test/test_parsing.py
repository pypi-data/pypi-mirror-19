# -*- coding: utf-8 -*-

import os
import glob
import sys
from importlib import import_module
import inspect
import math
import unittest
import argparse

import static_grader

simple_pair_list =  [
  [ "Jean Shafiroff",
    646
  ],
  [
    "Gillian Miniter",
    523
  ]]

simple_pair_as_dict = {
  'jean shafiroff': 646,
  'gillian miniter': 523
}

plural_key_list = [
  (("Japanese", "Food worker does not use proper utensil to eliminate bare hand contact with food that will not receive adequate additional heat treatment."), 3.26552598343535, 541),
  (("Café/Coffee/Tea", "?Choking first aid? poster not posted. ?Alcohol and pregnancy? warning sign not posted. Resuscitation equipment: exhaled air resuscitation masks (adult & pediatric); latex gloves; sign not posted. Inspection report sign not posted."), 3.14148182332827, 175)]
plural_key_as_dict = {(u'japanese',
   u'food worker does not use proper utensil to eliminate bare hand contact with food that will not receive adequate additional heat treatment.'):
  (3.26552598343535, 541),
 (u'caf\xe9/coffee/tea',
   u'?choking first aid? poster not posted. ?alcohol and pregnancy? warning sign not posted. resuscitation equipment: exhaled air resuscitation masks (adult & pediatric); latex gloves; sign not posted. inspection report sign not posted.'): (3.14148182332827, 175)}

already_a_dict = {
    "vet_views": 926.398240,
    "vet_score": 3.543454,
    "vet_favorites": 1.300880,
    "vet_answers": 1.298130,
    "brief_views": 557.671045,
    "brief_score": 2.108557,
    "brief_favorites": 0.579330,
    "brief_answers": 0.973072
}


list_of_strings =  [
  "Kirsten Bailey",
  "Kristina Stewart Ward"
]
list_of_strings_as_dict = {
  "kirsten bailey": 1,
  "kristina stewart ward": 1
}

class ParserTest(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_tuple_as_key_plural(self):
    parsed = static_grader.ListScorer.parse(plural_key_list,
                                      key_indices=(0,),
                                      value_indices=(1,2))
    self.assertEqual(parsed, plural_key_as_dict)

  def test_simple_pair(self):
    parsed = static_grader.ListScorer.parse(simple_pair_list)
    self.assertEqual(parsed, simple_pair_as_dict)

  def test_dict(self):
    parsed = static_grader.ListScorer.parse(already_a_dict)
    self.assertEqual(parsed, already_a_dict)



  def test_list_of_strings(self):
    parsed = static_grader.ListScorer.parse(list_of_strings, value_indices=None)
    self.assertEqual(parsed, list_of_strings_as_dict)



if __name__ == '__main__':
  unittest.main()
