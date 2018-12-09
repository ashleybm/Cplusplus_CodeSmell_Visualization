import unittest
import CodeParse

class Test_TestCodeParse(unittest.TestCase):
    
    def test_is_word(self):
        word = "words"
        self.assertTrue(CodeParse.is_word(word))

    def test_is_num(self):
        num = "21"
        self.assertTrue(CodeParse.is_num(num))