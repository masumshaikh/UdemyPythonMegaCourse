# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 22:03:44 2019

@author: e1081018
"""

import unittest
import os

from model import Model
from model import Record

class ModelTests(unittest.TestCase):

    # setUp() is done for every single test we run
    def setUp(self):
        if (os.path.exists("unittests.db")):
            os.remove("unittests.db")
            
        self.m = Model("unittests.db")
        self.m.populate_fake()        
   
#   TODO: Test update functionality.
#   TODO: Test that trying to delete a record with id that doesn't exist doesn't throw an exception.

    def test_expected_number_after_setUp(self):       
        # Test we have the expected number of items after setUp()
        self.assertEqual(12, self.m.num_records())
        self.assertEqual(self.m.num_records(), self.m.num_records())

    def test_get_single_record_given_id(self):
        self.assertEqual(self.m.get_records_with_id([2]), \
                         [(2, 'Midnight Rain', 'Ralls, Kim', 2000, 8280773308516)])
        
    def test_match_single_criterion_multiple_results(self):
        search_term = Record(title = None, author='Corets, Eva', year=None, isbn=None)
        expected = [(3, 'Maeve Ascendant', 'Corets, Eva', 2000, 7635451973929), \
                    (4, "Oberon's Legacy", 'Corets, Eva', 2001, 1503317573995), \
                    (5, 'The Sundered Grail', 'Corets, Eva', 2001, 2835673347453)]
        self.assertEqual(self.m.find_matching_records(search_term), expected)

    def test_match_two_criteria_single_result(self):
        search_term = Record(title = None, author='Corets, Eva', year=2000, isbn=None)
        expected = [(3, 'Maeve Ascendant', 'Corets, Eva', 2000, 7635451973929)]
        self.assertEqual(self.m.find_matching_records(search_term), expected)

    def test_match_two_criteria_two_results(self):
        search_term = Record(title = None, author='Corets, Eva', year=2001, isbn=None)
        expected = [(4, "Oberon's Legacy", 'Corets, Eva', 2001, 1503317573995), \
                    (5, 'The Sundered Grail', 'Corets, Eva', 2001, 2835673347453)]
        self.assertEqual(self.m.find_matching_records(search_term), expected)

    def test_delete_one_record_from_list(self):
        count = self.m.num_records()
        self.m.delete_records_with_id([1])
        self.assertEqual([], self.m.get_records_with_id([1]))
        self.assertEqual(count - 1, self.m.num_records())
        
    def test_delete_two_records_from_tuple(self):
        count = self.m.num_records()
        self.m.delete_records_with_id((2,3))
        self.assertEqual([], self.m.get_records_with_id([2,3]))
        self.assertEqual(count - 2, self.m.num_records())
        
    def test_delete_multiple_records_from_list(self):
        count = self.m.num_records()
        self.m.delete_records_with_id([4,5,6,7])       
        self.assertEqual([], self.m.get_records_with_id([4,5,6,7]))
        self.assertEqual(count - 4, self.m.num_records())
        
    def test_delete_multiple_records_from_range(self):
        count = self.m.num_records()
        self.m.delete_records_with_id(range(8,12))       
        self.assertEqual([], self.m.get_records_with_id(range(8,12)))
        self.assertEqual(count - 4, self.m.num_records())
        
    def test_expected_item_remaining(self):
        self.m.delete_records_with_id([1])
        self.m.delete_records_with_id((2,3))
        self.m.delete_records_with_id([4,5,6,7])    
        self.m.delete_records_with_id(range(8,12)) 
        self.assertEqual(self.m.get_all_records(), \
                         [(12, 'Visual Studio 7: A Comprehensive Guide', 'Galos, Mike', 2001, 2211388125058)])

if __name__ == '__main__':
    unittest.main()