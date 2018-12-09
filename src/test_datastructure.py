import unittest
import DataStructure
import CodeParse

class Test_TestDataStructure(unittest.TestCase):

    def test_is_class_true(self):
        segments_test = CodeParse.Segment("W",1,"class")
        segments_list = list()
        segments_list.append(segments_test)
        
        self.assertTrue(DataStructure.is_class(segments_list))

    def test_is_class_false(self):
        segments_test = CodeParse.Segment("S",1,"+")
        segments_list = list()
        segments_list.append(segments_test)
        
        self.assertFalse(DataStructure.is_class(segments_list))


    def test_is_method(self):
        segments_test = CodeParse.Segment("S",1,"(doing a thing)")
        segments_list = list()
        segments_list.append(segments_test)
        
        self.assertFalse(DataStructure.is_method(segments_list))


    