'''
The module to access and process the 
dictionary which is stored as json files
'''

import config
import json
import ast
from collections import namedtuple, Counter, OrderedDict
import pprint
import pū
import maoriword as mw


def get_all_entries():

    all_entries = {}
    Word_ID = namedtuple('Word_ID', 'root_number trunk branch_number twig twig_number')
    
    #gather all the parts and make one large ordered dictionary
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
    return OrderedDict(sorted(all_entries.items(), key=mw.get_dict_sort_key))


def get_headwords():
    '''
    The purpose of this method is to get all the headwords
    from HPK. 

    A headword is a unique 'root number, trunk' combination
    '''
    all_entries = get_all_entries()
    headwords = []
    headwords = list(set([(k.root_number, k.trunk) for k in all_entries.keys()]))
    return headwords


def get_passives(words_only = True):
    '''
    if words_only = True (default)    
    The purpose of this method is to get all the distinct passive words.
    
    if words_only = False 
    Will return an OrderedDict of only those twigs and branches
    that have passive endings.
    '''
    all_entries = get_all_entries()
    passives = {k:v for k,v in all_entries.items() if v["pīmuri_whakahāngū"]}
    
    if words_only:
        passive_words = []
        for k,v in passives.items():
            for suffix in [x for x in v["pīmuri_whakahāngū"] if x]:
                #the code to process suffixes resulted in 11 cases of passive suffixes = ''
                #so list comprehension (above) is used to weed these out.
                if suffix.startswith(chr(8209)): #looks like a '-'
                    #append to either the trunk or the twig
                    if k.twig is False:
                        #branch
                        passive_word = k.trunk + suffix[1:]
                    else:
                        #twig
                        passive_word = k.twig + suffix[1:]
                else:
                    passive_word = suffix #completely new word as passive
                passive_words.append(passive_word)
        
        passive_words = list(set(passive_words)) #unique only
        return sorted(passive_words, key=mw.get_list_sort_key)
                    
    else:
        return OrderedDict(sorted(passives.items(), key=mw.get_dict_sort_key))


def get_nominalisations(words_only = True):
    '''
    if words_only = True (default)    
    The purpose of this method is to get all the distinct nominalised words.
    
    if words_only = False 
    Will return an OrderedDict of only those twigs and branches
    that have nominalised endings.
    '''
    all_entries = get_all_entries()
    nominalisations = {k:v for k,v in all_entries.items() if v["pīmuri_whakaingoa"]}
    
    if words_only:
        nominalised_words = []
        for k,v in nominalisations.items():
            for suffix in [x for x in v["pīmuri_whakaingoa"] if x]:
                if not suffix:
                    print(k)
                if suffix.startswith(chr(8209)): #looks like a '-'
                    #append to either the trunk or the twig
                    if k.twig is False:
                        #branch
                        nominalised_word = k.trunk + suffix[1:]
                    else:
                        #twig
                        nominalised_word = k.twig + suffix[1:]
                else:
                    nominalised_word = suffix #completely new word as nominalised form
                nominalised_words.append(nominalised_word)
        
        nominalised_words = list(set(nominalised_words)) #unique only
        return sorted(nominalised_words, key=mw.get_list_sort_key)
                    
    else:
        return OrderedDict(sorted(nominalisations.items(), key=mw.get_dict_sort_key))


def get_twigs(words_only = True, on_trunk_only = False):
    '''
    The purpose of this function is to return all the twigs
    A twig is defined as an entry in the all_entries dictionary
    where there is a word in the 'twig' part of the namedtuple key.

    If there is a requirement to look at twigs that are directly
    on the trunk then set on_trunk_only = True

    words_only will return a list
    otherwise an OrderedDict of the twigs 
    '''
    all_entries = get_all_entries() 

    #all twigs
    twigs = {k:v for k,v in all_entries.items() if not k.twig is False}

    if on_trunk_only:   
        #subset of the twigs     
        twigs = {k:v for k,v in all_entries.items() if k.branch_number == 0}

    if words_only:
        twigs_list = [k.twig for k in twigs.keys()]
        twigs_list = list(set(twigs_list)) #unique only
        return sorted(twigs_list, key=mw.get_list_sort_key)
    else:
        return OrderedDict(sorted(twigs.items(), key=mw.get_dict_sort_key))


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
    all_entries = get_all_entries()
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
    


def get_children(input_string = 'pangakupu', 
                 minimum_length = 3, 
                 must_include_last_letter = True):
    '''
    Returns a list containing all the word forms (children)
    that can be made from the input_string
    '''

    children = []

    input_string_to_use = mw._aslist(input_string)

    unique_word_forms = get_word_forms()
    for word in [x for x in unique_word_forms if len(x) >= minimum_length]:

        word_to_use = mw._aslist(word)

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
    import argparse
    import pprint
    import ast

    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the get_all_entries function
    get_all_entries_parser = subparsers.add_parser('get_all_entries', help = '>>>>>> No arguments')
    get_all_entries_parser.set_defaults(function = get_all_entries)

    # create the parser for the get_headwords function
    get_headwords_parser = subparsers.add_parser('get_headwords', help = '>>>>>> No arguments')
    get_headwords_parser.set_defaults(function = get_headwords)

    # create the parser for the get_passives function
    get_passives_parser = subparsers.add_parser('get_passives')
    get_passives_parser.add_argument('-words_only')
    get_passives_parser.set_defaults(function = get_passives)

    # create the parser for the get_nominalisations function
    get_nominalisations_parser = subparsers.add_parser('get_nominalisations')
    get_nominalisations_parser.add_argument('-words_only')
    get_nominalisations_parser.set_defaults(function = get_nominalisations)

    # create the parser for the get_twigs function
    get_twigs_parser = subparsers.add_parser('get_twigs')
    get_twigs_parser.add_argument('-words_only')
    get_twigs_parser.add_argument('-on_trunk_only')
    get_twigs_parser.set_defaults(function = get_twigs)

    # create the parser for the get_children function
    get_children_parser = subparsers.add_parser('get_children', help = '>>>>>> No arguments')
    get_children_parser.set_defaults(function = get_children)

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

        #alter any string 'True' or 'False' to bools
        arguments = { k : ast.literal_eval(v) for k,v in arguments.items() if v in ['True','False'] }       

    result = function_to_call(**arguments) #note **arguments works fine for empty dict {}
   
    print (len(result))
    print (type(result))
    #pprint.pprint(result)
    for k,v in result.items():
        print(k)


