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

class MaoriWord():
    digraphs = ('wh','ng','WH','NG','Wh','Ng','wH','nG')
    
    vowels = ('a', 'e', 'i', 'o', 'u',
              'A', 'E', 'I', 'O', 'U')
    
    macronised_vowels = ('ā', 'ē', 'ī', 'ō', 'ū',
                         'Ā', 'Ē', 'Ī', 'Ō', 'Ū')
    
    consonants = ('h', 'k', 'm', 'n', 'p', 'r', 't', 'w',
                  'H', 'K', 'M', 'N', 'P', 'R', 'T', 'W')
    
    legal_letters = digraphs + vowels + macronised_vowels + consonants
    
    legal_punctuation = (' ', '-')
    
    def __init__(self, word):

        self.word = word

        if self.isnoncompound():
            # no legal punctation (*one* 'word')
            # check to see if all the letters are legal
            if self.legalletters():
                pass
            else:
                # illegal letters
                print('illegal letters')
                exit
            
        else:
            # contains legal punctation (compound)
            print ('compound')
         
    

    def isnoncompound(self):
        
        for lp in self.legal_punctuation:
            if lp in self.word:
                return False
        return True    


    def iscompound(self):
        '''a compound word contains 2 or more non-compound words
        separated by legal punctuation'''
        words = (re.split("|".join(lp[0] for lp in self.legal_punctuation),
                          self.maori_word))
        
        is_compound_word = True
        
        for w in words:
            try:
                MaoriWord(w)
            except:
                is_compound_word = False
                
        return is_compound_word    

    def endsinvowel(self):
        if self.word[-1:] in self.vowels + self.macronised_vowels:
            return True
        else:
            return False

    def legalletters(self):
        if set(self.aslist()).issubset(self.legal_letters):
            return True
        else:
            return False

    def isconsonantvowel(self):

        if not self.word.endsinvowel():
            return False

        pairs = (list(zip(self.word.aslist(),
                          self.word.aslist()[1:])))     
             
        #assume that the word is well formed
        #that is every consonant is followed by a vowel
        return_value = True
        
        for p in pairs:
            #print (p)
            if p[0] in self.digraphs + self.consonants:
                #next letter has to be a vowel
                if p[1] not in self.vowels + self.macronised_vowels:
                    return_value = False #word is not well formed
                    break
                    
        return return_value   

    def aslist(self):
        '''take a string and convert to list - allowing for digraphs'''

        return_list = []

        pairs = (list(zip(self.word,
                          self.word[1:] + " ")))

        check_pair = True
        
        for p in pairs:
            pair = p[0] + p[1]
            
            if check_pair:
                if pair in self.digraphs:
                    return_list.append(pair)
                    #the next pair can't be a digraph
                    check_pair = False
                else:
                    return_list.append(p[0])
            else:
                check_pair = True                    
                
        return return_list        

    def demacronise(self):
        temp_string = self.maori_word
        for mv in self.macronised_vowels:
            temp_string = temp_string.replace(mv, unicodedata.normalize('NFD',mv)[0])
        demacronised_string = temp_string    
        return demacronised_string
        
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

if __name__ == '__main__':
    print(MaoriWord('hj'), 'main')

