'''
The module to access the json files
I'm not really sure what it does as yet
'''

import config
import json
import ast
from collections import namedtuple, Counter
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

def bar(z, y='supersplodge'):
    print ('y', y)
    print ('z', z)
    pass

    
if __name__ == '__main__':

    import sys
    import argparse

    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the get_all_entries function
    get_all_entries_parser = subparsers.add_parser('get_all_entries')
    get_all_entries_parser.set_defaults(function = get_all_entries)

    # create the parser for the "bar" command
    parser_bar = subparsers.add_parser('bar')
    parser_bar.add_argument('-z')
    parser_bar.add_argument('-y')
    parser_bar.set_defaults(function = bar)

    # parse the arguments
    arguments = parser.parse_args()
    arguments = vars(arguments) #convert from Namespace to dict

    #attempt to extract and then remove the function entry
    try:
        function_to_call = arguments['function'] 
    except KeyError:
        #python pataka.py entered on command line (a function name is required)
        print ("You need a function name. Please type -h to get help")
        sys.exit()
    else:
        #remove the function entry
        del arguments['function']
    
    if arguments:
        #remove any entries that have a value of 'None'
        #We are *assuming* that these are optional
        #We are doing this because we want the function definition to define
        #the defaults (NOT the function call)
        arguments = { k : v for k,v in arguments.items() if v is not None }
    
    result = function_to_call(**arguments) #note **arguments works fine for empty dict {}
   
    #print (len(result))



