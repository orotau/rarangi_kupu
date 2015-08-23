import pytest
from unicodedata import normalize
import pataka
import pū
from collections import Counter

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
