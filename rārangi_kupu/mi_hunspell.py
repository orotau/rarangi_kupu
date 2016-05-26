'''
The module to help create the dic and aff files for hunspell 
'''

import pataka
import pprint
import itertools

def get_all_suffixes():
    '''
    The purpose of this function is to get every entry
    in HPK that has a suffix.

    There is no distinction between passive suffixes and
    nominalisation suffixes (at least at this stage)
    i.e. they will be lumped into one list

    returns a dictionary 

    a sample key : value pair

    Word_ID(root_number=1, trunk='paraparau', branch_number=2, twig=False, 
    twig_number=0): ['‑tanga', '‑ngia', '‑hia', '‑tia']

    '''

    all_suffixes = {}  
    passives = pataka.get_passives(False)
    nominalisations = pataka.get_nominalisations(False)

    all_keys = passives.keys() | nominalisations.keys() # union

    for key in all_keys:
        try:
            passives[key]
        except KeyError:
            # the key is not in the passives dictionary
            # it must be in the nominalisations dictionary
            all_suffixes[key] = nominalisations[key]["pīmuri_whakaingoa"]
        else:
            # the key is in the passives dictionary
            try:
                nominalisations[key]
            except KeyError:
                # the key is in ONLY the passives dictionary
                all_suffixes[key] = passives[key]["pīmuri_whakahāngū"]
            else:
                # the key is in BOTH dictionaries
                all_suffixes[key] = nominalisations[key]["pīmuri_whakaingoa"] + \
                                    passives[key]["pīmuri_whakahāngū"]
    print (all_suffixes)
    return all_suffixes


def get_distinct_suffixes (word_form = "all"):
    '''
    The purpose of get_distinct_suffixes
    is to get the distinct suffixes for the word_form passed

    If no word_form is passed then all 'word forms' with suffixes
    will be found

    Empty suffixes (an error in the data) will be excluded

    Return a dictionary with the following form

    A Sample key : value pair

    'paraparau' : {'‑tanga', '‑ngia', '‑hia', '‑tia'}

    The code ASSUMES (correct as at May 2016) that there are no 'twigs'
    '''

    distinct_suffixes = {}
    all_suffixes = get_all_suffixes()
    all_suffixes_copy = all_suffixes # hack, see below

    if word_form != "all":
        # get all the possible suffixes for the word_form passed
        word_form_suffixes = {k : v for k, v in all_suffixes.items() if k.trunk == word_form}
        print(word_form_suffixes)

        # list of lists of all possible suffixes
        all_possible_suffixes = word_form_suffixes.values()

        # flatten list of lists to get a list
        all_suffixes = itertools.chain.from_iterable(all_possible_suffixes)

        #remove any '' suffixes
        all_suffixes = [x for x in all_suffixes if x]

        # create dictionary entry of set of suffixes to return
        distinct_suffixes[word_form] = set(all_suffixes)

    else:
        for k, v in all_suffixes.items():
            # not proud of this code but it seems to work!
            word_form = k.trunk
            if word_form not in distinct_suffixes:
                # get all keys that share the same word_form
                word_form_suffixes = {k : v for k, v in all_suffixes_copy.items() if k.trunk == word_form}

                # list of lists of all possible suffixes for the word_form
                all_possible_suffixes = word_form_suffixes.values()

                # flatten list of lists to get a list
                all_suffixes = itertools.chain.from_iterable(all_possible_suffixes)

                #remove any '' suffixes
                all_suffixes = [x for x in all_suffixes if x]

                # create dictionary entry of set of suffixes to return
                distinct_suffixes[word_form] = set(all_suffixes)
                

    return distinct_suffixes

def get_distinct_suffix_groups():
    '''
    get the distinct suffix groups
    return a list of sets
    '''
    distinct_suffixes = get_distinct_suffixes()

    # list of sets
    distinct_suffix_groups = list(distinct_suffixes.values())

    # list of sorted tuples
    distinct_suffix_groups = [tuple(sorted(list(x))) for x in distinct_suffix_groups]

    # distict suffix groups    
    return set(distinct_suffix_groups)


if __name__ == '__main__':

    import argparse
    import sys
    import ast
    import pprint

    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the get_all_entries function
    get_all_entries_parser = subparsers.add_parser('get_all_suffixes')
    get_all_entries_parser.set_defaults(function = get_all_suffixes)

    # create the parser for the get_distinct_suffixes function
    get_distinct_suffixes_parser = subparsers.add_parser('get_distinct_suffixes')
    get_distinct_suffixes_parser.add_argument('-word_form')
    get_distinct_suffixes_parser.set_defaults(function = get_distinct_suffixes)

    # create the parser for the get_distinct_suffix_groups function
    get_distinct_suffix_groups_parser = subparsers.add_parser('get_distinct_suffix_groups')
    get_distinct_suffix_groups_parser.set_defaults(function = get_distinct_suffix_groups)

    # parse the arguments
    arguments = parser.parse_args()
    arguments = vars(arguments) #convert from Namespace to dict

    #attempt to extract and then remove the function entry
    try:
        function_to_call = arguments['function'] 
    except KeyError:
        #python mi_hunspell.py entered on command line (a function name is required)
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
        arguments = { k : ast.literal_eval(v) if v in ['True','False'] else v 
                                              for k,v in arguments.items() }       

    result = function_to_call(**arguments) #note **arguments works fine for empty dict {}

    pprint.pprint(result)
    print(len(result))
