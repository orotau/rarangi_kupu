import pytest
from unicodedata import normalize
import pataka
import pū
from collections import Counter
import config
import json
import maoriword as mw

def test_headword_counts():

    #count the headwords for each dictionary letter (for cross checking)
    dictionary_letters = []
    for hw in [x[1] for x in pataka.get_headwords()]:
        if hw.startswith('-'):
            #if a headword starts with a dash, the dash (not the word) is ignored
            hw = hw[1:]

        if any(hw.startswith(x) for x in pū.digraphs):
            #the headword starts with a digraph
            dictionary_letters.append(hw[0:1].upper() + hw[1:2]) #Ng or Wh
        else:
            #the headword doesn't start with a digraph
            #remove any macron and make uppercase
            dictionary_letters.append(normalize('NFD', hw[0:1].upper())[0])

    c = Counter(dictionary_letters)
    assert dict(c) ==   {'A': 621,
                         'E': 57,
                         'H': 1246,
                         'I': 156,
                         'K': 2332,
                         'M': 1309,
                         'N': 228,
                         'Ng': 282,
                         'O': 167,
                         'P': 2061,
                         'R': 684,
                         'T': 2631,
                         'U': 153,
                         'W': 299,
                         'Wh': 1132}

    assert len(dictionary_letters) == 13358
    assert sum(dict(c).values()) == 13358

def test_pangakupu_words():

    cf = config.ConfigFile()
    json_path = (cf.configfile[cf.computername]['iwa_path'])
    json_filename = "all_words_for_iwa.json"
    full_json_path = json_path + json_filename
    with open(full_json_path,'r') as f:
        all_words_for_iwa = json.load(f)

    #word counts
    assert len(all_words_for_iwa) == 11601
    c = Counter(len(x) for x in all_words_for_iwa)
    assert dict(c) == {1: 9,
                       2: 57,
                       3: 255,
                       4: 1099,
                       5: 1169,
                       6: 2691,
                       7: 1568,
                       8: 1949,
                       9: 830,
                       10: 971,
                       11: 451,
                       12: 279,
                       13: 164,
                       14: 54,
                       15: 35,
                       16: 10,
                       17: 6,
                       18: 3,
                       19: 1}

    assert sum(dict(c).values()) == 11601 #recheck the count
    assert sum([k * v for k, v in dict(c).items()]) == 83080
    assert len(set(all_words_for_iwa)) == 11601 #test for uniqueness
    
    #check every entry is lower case
    assert [x if x.lower() == x else 'derp' for x in all_words_for_iwa] == all_words_for_iwa

    #check every entry is free of punctuation
    assert [x if mw._isalllegalletters(x) else 'derp' for x in all_words_for_iwa] == all_words_for_iwa

    #check that the basics for all maori words hold
    for x in all_words_for_iwa:
        assert x == mw.MaoriWord(x).word

    #letter counts
    all_letters_for_iwa = []
    for x in all_words_for_iwa:
        all_letters_for_iwa.extend(mw._aslist(x))
    c = dict(Counter(all_letters_for_iwa))
    assert c == {'a': 14894,
                 'ā': 2252,
                 'e': 5125,
                 'ē': 281,
                 'h': 3970,
                 'i': 6765,
                 'ī': 627,
                 'k': 6882,
                 'm': 2406,
                 'n': 2002,
                 'ng': 1834,
                 'o': 5521,
                 'ō': 1216,
                 'p': 3733,
                 'r': 6270,
                 't': 5880,
                 'u': 5736,
                 'ū': 993,
                 'w': 1245,
                 'wh': 1807}

    assert sum(dict(c).values()) == 79439 #digraphs count as 1 letter

    #cross check letter counts from words vs direct letter counts
    assert 83080 == 79439 + c['ng'] + c['wh'] #digraphs count as 2 letters
