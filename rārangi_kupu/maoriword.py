'''What is going on - this needs to be described..
   Strange behaviour - need to document purpose!

   A word will be initialised if the following conditions hold

   1) The word is non-compound (does *not* contain legal punctuation)
   AND
      The word only contains legal letters
   AND
      Every consonant is followed by a vowel

   or

   2) The word is compound (does contain legal punctuation)
   AND
      Each word passes all of test 1) above

   I would like to make the compound words part of a different class
   but I don't know how to do that yet....

   also if we pass in '' what should happen?
'''
import unicodedata
import re
from rārangi_kupu import pū


class MaoriWord():
    
    def __init__(self, word):

        if word.strip() != word:
            #the word has leading and/or trailing whitespace
            raise ValueError

        if word.strip() == '':
            #empty string
            raise ValueError

        #check that we have all legal characters
        if not _isalllegalcharacters(word):
            raise ValueError

        #split by punctuations
        for part in _word_split(word):
            #check it ends in a vowel
            if not _endsinvowel(part):
                raise ValueError
            if not _isconsonantvowel(part):
                raise ValueError

        self.word = word

    def getKey(self):
        #Key 1 - Letters
        key1 = self.demacronise()
        key1 = key1.lower()
        key1 = MaoriWord(key1).aslist()        

        #Key 2 - Macrons
        key2 = self.maori_word.lower()
        key2 = MaoriWord(key2).aslist()

        #Key 3 - Case
        key3 = self.aslist() #upper case first (as per HPK)
      
        return key1, key2, key3

    def __repr__ (self):
        return self.word

def _isalllegalcharacters(word):
    if set(_aslist(word)).issubset(pū.all_legal_characters):
        return True
    else:
        return False

def _isconsonantvowel(word):

    if word.strip() != word:
        #the word has leading and/or trailing whitespace
        return False

    pairs = (list(zip(_aslist(word),
                      _aslist(word)[1:])))     
         
    #assume that the word is well formed
    #that is every consonant is followed by a vowel
    return_value = True
    
    for p in pairs:
        #print (p)
        if p[0] in pū.digraphs + pū.consonants:
            #next letter has to be a vowel

            if p[1] not in pū.vowels + pū.macronised_vowels:
                return_value = False #word is not well formed
                break
                
    return return_value

def _word_split(word):
    '''split the word into 1 or more words separated
    by the punctuation'''
    words = (re.split("|".join(lp[0] for lp in pū.legal_punctuation),
                      word))
    return words   

def _aslist(word):
    '''take a string and convert to list - allowing for digraphs'''

    return_list = []

    pairs = (list(zip(word,
                      word[1:] + " ")))

    check_pair = True
    
    for p in pairs:
        pair = p[0] + p[1]
        
        if check_pair:
            if pair in pū.digraphs:
                return_list.append(pair)
                #the next pair can't be a digraph
                check_pair = False
            else:
                return_list.append(p[0])
        else:
            check_pair = True                    
            
    return return_list

def _endsinvowel(word):
    if word[-1:] in pū.vowels + pū.macronised_vowels:
        return True
    else:
        return False

def _demacronise(word):
    for mv in pū.macronised_vowels:
        word = word.replace(mv, unicodedata.normalize('NFD',mv)[0])
    demacronised_string = word    
    return demacronised_string

if __name__ == '__main__':
    print(MaoriWord('hj'), 'main')

