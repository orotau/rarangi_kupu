'''
The module to access the json files
I'm not really sure what it does as yet
'''

import config
import json
import ast
from collections import namedtuple, Counter
from unicodedata import normalize
import pprint
import pū
import maoriword as mw

all_entries = {}

def get_all_entries():

    Word_ID = namedtuple('Word_ID', 'root_number trunk branch_number twig twig_number')
    
    #gather all the parts and make one large dictionary

    cf = config.ConfigFile()
    json_path = (cf.configfile[cf.computername]['json_path'])

    for letter in pū.dictionary_letters:
        print ('gathering json', letter)
        json_filename = letter + ".json"
        full_json_path = json_path + json_filename
        with open(full_json_path,'r') as f:
            word_trees_from_json = json.load(f)

        word_trees_from_json = {Word_ID(**ast.literal_eval(k)):v for k,v in word_trees_from_json.items()}
        all_entries.update(word_trees_from_json)
    print (len(all_entries))
    temp = []
    for k,v in all_entries.items():
        if k.trunk == 'mano':
            temp.append(k)
    pprint.pprint (sorted(temp, key=mw.get_dict_sort_key))
    return sorted(all_entries, key=mw.get_dict_sort_key)


def get_headwords():
    '''
    The purpose of this method is to get all the headwords
    from HPK. 

    A headword is a unique 'root number, trunk' combination
    '''

    if not all_entries:
        get_all_entries()
    headwords = []
    headwords = list(set([(k.root_number, k.trunk) for k in all_entries.keys()]))

    #count the headwords for each dictionary letter (for cross checking)
    dictionary_letters = []
    for hw in [x[1] for x in headwords]:
        if hw.startswith('-'):
            #if a headword starts with a dash, it is ignored
            hw = hw[1:]

        if any(hw.startswith(x) for x in pū.digraphs):
            #the headword starts with a digraph
            dictionary_letters.append(hw[0:1].upper() + hw[1:2]) #Ng or Wh
        else:
            #the headword doesn't start with a digraph
            #remove any macron and make uppercase
            dictionary_letters.append(normalize('NFD', hw[0:1].upper())[0])

    c = Counter(dictionary_letters)
    pprint.pprint(sorted(c.most_common()))
    return headwords


def get_passives():
    '''
    The purpose of this method is to get all of the passives 
    suffixes for all the words (at this point)
    '''

    if not all_entries:
        get_all_entries()
    passives = []
    for k,v in all_entries.items():
        if v["pīmuri_whakahāngū"]:
            passives.append(k)
    return sorted(passives, key=mw.get_dict_sort_key)
        

def get_twigs(on_trunk_only = False):

    if not all_entries:
        get_all_entries() 
    twigs = []    
    for k,v in all_entries.items():
        if not k.twig is False:
            if k.branch_number == 0:
                twigs.append(k)
    return sorted(twigs, key=mw.get_dict_sort_key)


def get_word_forms():
    '''
    The purpose of this function is to return all of the word forms
    from HPK.
    A word form is by definition unique
    all twigs and 
    all compound words and
    any word which has uppercase letters in it
    will be *excluded*
    passives and nominalisations to be dealt with later
    '''
    if not all_entries:
        get_all_entries()
    word_forms = []

    for k,v in all_entries.items():
        include = True
        
        if not k.twig is False:
            #its a twig
            include = False

        if any(x in k.trunk for x in pū.intra_word_punctuation):
            include = False

        if pū.inter_word_punctuation in k.trunk:
            include = False

        if k.trunk != k.trunk.lower():
            include = False

        if include:
            word_forms.append(k.trunk)

    word_forms = list(set(word_forms)) #only unique
    return sorted(word_forms, key=mw.get_list_sort_key)
    #return sorted(word_forms, key=len)    
    


def get_children(input_string = 'pungakupa', 
                 minimum_length = 3, 
                 split_digraphs = False,
                 must_include_last_letter = True):
    '''
    Returns a list containing all the word forms (children)
    that can be made from the input_string
    '''

    children = []

    if not split_digraphs: #default
        input_string_to_use = mw._aslist(input_string)
    else:
        input_string_to_use = input_string

    unique_word_forms = get_word_forms()
    for word in [x for x in unique_word_forms if len(x) >= minimum_length]:

        if not split_digraphs: #default                       
            word_to_use = mw._aslist(word)
        else:
            word_to_use = word

        is_child = False            
        if not (Counter(word_to_use) - Counter(input_string_to_use)):
            is_child = True

        if is_child:
            if must_include_last_letter:
                if input_string[-1] in word:
                    children.append(word)    
            else:
                #it's a child and we don't care if it includes last letter or not
                children.append(word)
    return(children)

    
if __name__ == '__main__':
    import sys
    import pprint
    import inspect
    import ast

    try:
        first_argument = sys.argv[1]
    except IndexError:
        #No argument given
        print ("Please supply a function name")
        sys.exit()

    function_to_call = getattr(sys.modules[__name__], first_argument)
    result = function_to_call()

    pprint.pprint(result)
    print (len(result))


