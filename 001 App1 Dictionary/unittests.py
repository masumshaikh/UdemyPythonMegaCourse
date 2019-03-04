# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 13:02:49 2019

@author: e1081018
"""

import unittest
from DictApp import DictApp
from DictApp import DefinitionsHelper

class TestStringMethods(unittest.TestCase):

    dictapp = DictApp()
    def test_garbage(self):
        defns = self.dictapp.try_get_definitions('lkjkasldkfjalsdkjalsdkjf')
        self.assertEqual(str(defns), DefinitionsHelper.msg_not_found)

    def test_emtpydef(self):
        emptydef = DefinitionsHelper()
        self.assertEqual(str(emptydef), DefinitionsHelper.msg_not_found)

    def test_singleword_singledef(self):
        singledef = DefinitionsHelper()
        singledef.add("word", ["singledef"])
        self.assertEqual(str(singledef), "\nword:\n1.\tsingledef\n")

    def test_singleword_twodefs(self):
        twodefs = DefinitionsHelper()
        twodefs.add("word", ["firstdef", "seconddef"])
        self.assertEqual(str(twodefs), "\nword:\n1.\tfirstdef\n\n2.\tseconddef\n")

    def test_twowords_singledefeach(self):
        expected = DefinitionsHelper.msg_close_matches_found
        expected += "\nword, closematch\n"
        expected += "\nword:\n1.\tsingledef\n"
        expected += "\nclosematch:\n1.\tsingledef2\n"
        
        dfh = DefinitionsHelper()
        dfh.add("word", ["singledef"])
        dfh.add("closematch", ["singledef2"])
        self.assertEqual(str(dfh), expected)


if __name__ == '__main__':
    unittest.main()