import sys
import unittest

sys.path.append('C:\\Users\\oligra\\OneDrive\\__HPK')
import hpk_maoriword

class TestMaoriWordFunctions(unittest.TestCase):

    allowable_maori_words = ['mahi',
                             'putururu',
                             'a',
                             'Ā',
                             'awe awe',
                             'a-ahi']
    
    non_maori_words = ['ng',
                       'zebra',
                       'awe^awe',
                       'wah',
                       'puturur',
                       'a  a',
                       'a -']

    def setUp(self):
        pass

    def test_allowable_maori_words(self):
        for amw in self.allowable_maori_words:
            print(amw, 'durp')
            self.assertNotEqual (hpk_maoriword.MaoriWord(amw), ValueError)

    def test_non_maori_words(self):
        for nmw in self.non_maori_words:
            print (nmw, 'durpy')
            self.assertEqual (hpk_maoriword.MaoriWord(nmw), ValueError)
                    
if __name__ == '__main__':
    unittest.main()
