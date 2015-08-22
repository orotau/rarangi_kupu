'''
This module contains a class and some functions
I wasn't sure whether to put the function inside the class
or not.
I got very confused and so ended up putting the functions outside
the class.
I started them with an underscore but don't know if that was the
'right' thing to do. Some idea of 'only to be used internally'
There is considerable testing for this module made using
pytest which was 

a) Easy to use
b) Helped me to see that I need to rearrange my code because
it was hard to test.

I am at the point now 1 August 2015 where I can safely give
the sorting information to the Unicode people.

'''
import unicodedata
import re
import pū
import hpk


class MaoriWord():
    
    def __init__(self, word):

        #split by intra word punctuations
        for part in _word_split(word):

            #check the part has no leading and/or trailing whitespace
            if part.strip() != part:
                print ('1', word)
                raise ValueError

            #check the part is not the empty string
            if part.strip() == '':
                print ('2', word)
                raise ValueError

            #check that part has all legal letters
            if not _isalllegalletters(part):
                print ('3', word, part)
                raise ValueError

            #check part ends in a vowel
            if not _endsinvowel(part):
                print ('4', word)
                raise ValueError

            #check part is consonant vowel
            if not _isconsonantvowel(part):
                print ('5', word)
                raise ValueError

        self.word = word

    def __repr__ (self):
        return self.word


def get_list_sort_key(words_input):

    #Split the words input into a list
    words_input = _words_split(words_input)

    #join the words (if they check out ok)
    words_input_joined = ''
    for word_input in words_input:
        #Ensure each word is well structured
        word = MaoriWord(word_input).word
        words_input_joined = words_input_joined + word

    #Remove any intra word punctuation
    word = _remove_intra_word_punctuation(words_input_joined)

    #Key 1 - Letters
    key1 = _demacronise(word)
    key1 = key1.lower()
    key1 = _aslist(key1)

    #Key 2 - Macrons
    key2 = word.lower()
    key2 = _aslist(key2)

    #Key 3 - Case
    key3 = _aslist(word) #upper case first (as per HPK)
  
    return key1, key2, key3


def get_dict_sort_key(named_tuple_input):

    '''
    This method takes as input a named tuple in the form
    Word_ID(root_number, trunk, branch_number, twig, twig_number)
    and returns a key suitable for sorting dictionary
    entries as they are in HPK

    The key being
    list sort key, root number, branch number, twig_number

    '''
    word_form = named_tuple_input.trunk

    #if we have a suffix remove the - at the end of it
    if word_form.endswith(hpk.end_dash):
        word_form = word_form[:-1]

    #if we have a prefix remove the - at the start of it
    if word_form.startswith(hpk.start_dash):
        word_form = word_form[1:]
  
    #if we have a kīanga remove the ellipsis at the end of it
    if word_form.endswith(hpk.ellipsis):
        word_form = word_form[:-6]

    #if we have kawititanga o te ringa(ringa) remove the (ringa)
    if word_form == hpk.kotrr:
        word_form = word_form[:-7]

    #if we have E koe (E koe e koe) remove the  (E koe e koe)
    if word_form == hpk.ekekek:
        word_form = word_form[:-14] #including the space before the bracket 

    #if we have 'tahi (i te) tahua' remove the brackets
    if word_form == hpk.titt:
        word_form = word_form.replace('(','').replace(')','')

    #if we have 'takahi (i te) whare' remove the brackets
    if word_form == hpk.titw:
        word_form = word_form.replace('(','').replace(')','')

    #if we have 'hohou (i te) rongo' remove the brackets
    if word_form == hpk.hitr:
        word_form = word_form.replace('(','').replace(')','')

    #if we have 'mataono (rite)' remove the brackets
    if word_form == hpk.mr:
        word_form = word_form.replace('(','').replace(')','')

    #if we have 'E nge.' remove the . at the end of it
    if word_form == hpk.en_dot:
        word_form = word_form[:-1]    

    root_number = named_tuple_input.root_number
    branch_number = named_tuple_input.branch_number
    twig_number = named_tuple_input.twig_number
    list_sort_key = get_list_sort_key(word_form)
    return list_sort_key, root_number, branch_number, twig_number
    

def _isalllegalletters(word):
    if set(_aslist(word)).issubset(pū.all_letters):
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
    '''split the word into 1 or more parts separated
    by the intra word punctuation'''
    parts = (re.split("|".join(iwp[0] for iwp in pū.intra_word_punctuation),
             word))
    return parts

def _words_split(words):
    '''split the words into a list of individual words'''
    #This will need to be reworked if we have more than 1 piece of
    #inter word punctuation
    words = words.split(pū.inter_word_punctuation)
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

def _remove_intra_word_punctuation(word):
    for p in pū.intra_word_punctuation:
        word = word.replace(p, '')
    return word
