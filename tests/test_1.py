import rārangi_kupu.maoriword as mw
import pytest

def test_leading_and_or_trailing_whitespace():
    with pytest.raises(ValueError):
        mw.MaoriWord('  mana') #leading
        mw.MaoriWord('  mana    ') #leading and trailing
        mw.MaoriWord('mana  ') # trailing

def test_whitespace_or_empty():
    with pytest.raises(ValueError):
        mw.MaoriWord('') #empty
        mw.MaoriWord('      ') #whitespace


def test_word_as_list():
    #check the aslist method that converts the word to a list that allows for digraphs
    assert mw._aslist('mana') == list('mana') #should perform identically to list when no digraphs
    assert mw._aslist('ngutu') != list('ngutu')
    assert mw._aslist('ngutu') == ['ng','u','t','u']
    assert mw._aslist('whakangaro') == ['wh', 'a', 'k', 'a', 'ng', 'a', 'r', 'o']
    assert mw._aslist('WhĀnGa') == ['Wh', 'Ā', 'nG', 'a']
    assert mw._aslist('awe awe') == list('awe awe')


def test_all_legal_characters():
    #check the method that checks that the word consists of legal characters only
    assert mw._isalllegalcharacters('aeiou') == True
    assert mw._isalllegalcharacters('whakangākau') == True
    assert mw._isalllegalcharacters('wakangākau') == True #missing h but all legal characters
    assert mw._isalllegalcharacters('x') == False
    assert mw._isalllegalcharacters('whakagākau') == False  #missed the 'n' leaving 'g' which is illegal


def test_word_split():
    assert mw._word_split('awe awe') == ['awe','awe']
    assert mw._word_split('a-ahi') == ['a','ahi']
    assert mw._word_split('a- ahi') == ['a', '', 'ahi'] #repeated separators


def test_ends_in_vowel():
    assert mw._endsinvowel('awe') == True
    assert mw._endsinvowel('ā') == True
    assert mw._endsinvowel('huhy') == False


def test_is_consonant_vowel():
    assert mw._isconsonantvowel('awe') == True
    assert mw._isconsonantvowel('awe ') == False
    assert mw._isconsonantvowel('whanau') == True
    assert mw._isconsonantvowel('WHANGAREI') == True


def test_initialisation():
    assert mw.MaoriWord('utu').word == 'utu'
    assert mw.MaoriWord('Korekore-piri-ki-ngā-Tangaroa').word == 'Korekore-piri-ki-ngā-Tangaroa'
    assert mw.MaoriWord('āēīōĀĒĪŌŪ').word == 'āēīōĀĒĪŌŪ'
    with pytest.raises(ValueError):
        mw.MaoriWord('x')
        mw.MaoriWord('whakagākau') #missed the 'n' leaving 'g' which is illegal
        mw.MaoriWord('a- ahi') #repeated separators
        mw.MaoriWord('huhy')
