'''
The module to help create the dic and aff files for hunspell 
'''

import pataka
import pprint
import itertools
import maoriword as mw
import suffix_problems as sp


def get_all_entries_with_suffixes():
    '''
    The purpose of this function is to get every entry
    in HPK that has a suffix.

    There is no distinction between passive suffixes and
    nominalisation suffixes (at least at this stage)
    i.e. they will be lumped into one list

    returns a dictionary 

    a sample key : value pair

    Word_ID(root_number=1, trunk='paraparau', branch_number=2, twig=False, 
    twig_number=0): ['-tanga', '-ngia', '-hia', '-tia']

    Note that this function also replaces all chr(8209) hyphen characters
    that are used in the original data 
    with the standard hyphen chr(45) (they are visually equivalent)
    '''

    all_entries_with_suffixes = {}  
    passives = pataka.get_passives(False)
    nominalisations = pataka.get_nominalisations(False)

    all_keys = passives.keys() | nominalisations.keys() # union

    for key in all_keys:
        try:
            passives[key]
        except KeyError:
            # the key is not in the passives dictionary
            # it must be in the nominalisations dictionary
            all_entries_with_suffixes[key] = nominalisations[key]["pīmuri_whakaingoa"]
        else:
            # the key is in the passives dictionary
            try:
                nominalisations[key]
            except KeyError:
                # the key is in ONLY the passives dictionary
                all_entries_with_suffixes[key] = passives[key]["pīmuri_whakahāngū"]
            else:
                # the key is in BOTH dictionaries
                all_entries_with_suffixes[key] = nominalisations[key]["pīmuri_whakaingoa"] + \
                                                 passives[key]["pīmuri_whakahāngū"]
 
    # remove any '' suffixes (not sure why there are any but there are!)   
    all_entries_with_suffixes = \
    {k: [x for x in v if x] for k, v in all_entries_with_suffixes.items()}     

    # Change hyphens to 'normal' ones   
    all_entries_with_suffixes = \
    {k: [x.replace(chr(8209), chr(45)) for x in v] \
    for k, v in all_entries_with_suffixes.items()} 

    return all_entries_with_suffixes


def get_distinct_suffixes_for_word_form (word_form = "all"):
    '''
    The purpose of get_distinct_suffixes
    is to get the distinct suffixes for the word_form passed

    If no word_form is passed then all 'word forms' with suffixes
    will be found

    Return a dictionary with the following form

    A Sample key : value pair

    'paraparau' : ('-tanga', '-ngia', '-hia', '-tia')

    The code ASSUMES (correct as at May 2016) that there are no 'twigs'
    '''

    all_entries_with_suffixes = get_all_entries_with_suffixes()
    all_distinct_word_forms_with_suffixes = {}

    # squash the dictionary so that each distinct word form has 
    # one and only one entry
    for k, v in all_entries_with_suffixes.items():
        all_distinct_word_forms_with_suffixes.setdefault(k.trunk, []).append(v)            

    # flatten list of lists to one list of suffixes
    all_distinct_word_forms_with_suffixes = \
    {k : list(itertools.chain.from_iterable(v)) for k, v in \
    all_distinct_word_forms_with_suffixes.items()}

    # make the list of suffixes unique
    all_distinct_word_forms_with_suffixes = \
    {k : set(v) for k, v in \
    all_distinct_word_forms_with_suffixes.items()}

    # convert to a sorted tuple
    all_distinct_word_forms_with_suffixes = \
    {k : tuple(sorted(list(v))) for k, v in \
    all_distinct_word_forms_with_suffixes.items()}

    # sort out suffix problems
    for k, v in sp.suffix_problems.items():
        # check data
        assert all_distinct_word_forms_with_suffixes[k] == v[0]
        # update data
        all_distinct_word_forms_with_suffixes[k] = v[1] 

    if word_form == "all":
        return all_distinct_word_forms_with_suffixes
    else:
        try:
            return {word_form : all_distinct_word_forms_with_suffixes[word_form]}
        except KeyError:
            return {}
        

def get_distinct_suffix_groups():
    '''
    get the distinct suffix groups
    return a list of sorted tuples
    '''
    distinct_suffixes_for_word_form = get_distinct_suffixes_for_word_form()

    # list of sets
    distinct_suffix_groups = list(distinct_suffixes_for_word_form.values())

    # list of sorted tuples
    distinct_suffix_groups = [tuple(sorted(list(x))) for x in distinct_suffix_groups]

    # distinct suffix groups    
    return list(set(distinct_suffix_groups))


def assign_word_form_to_suffix_group (word_form = "all"):
    '''
    The purpose of this function is to take the word_form passed
    and assign it to the correct suffix group
    The group being one of the distinct suffix groups.

    If no parameter is passed this will be done for *all* word forms
    that have at least one suffix

    If the word_form passed has no suffix then {} will be returned

    otherwise a dictionary will be returned

    A Sample key : value pair

    ('-tanga', '-ngia', '-hia', '-tia') : ['paraparau', ...]

    The value will be sorted as Māori words
    '''

    suffix_groups_and_word_forms = {}
    distinct_suffixes_for_word_form = get_distinct_suffixes_for_word_form()
    for k, v in distinct_suffixes_for_word_form.items():
        if v not in suffix_groups_and_word_forms:
            suffix_groups_and_word_forms[v] = [k]
        else:
            suffix_groups_and_word_forms[v].append(k)

    # sort the word_forms    
    suffix_groups_and_word_forms = \
    {k: sorted(v, key=mw.get_list_sort_key) for k, v in \
    suffix_groups_and_word_forms.items()}

    return suffix_groups_and_word_forms

def get_distinct_suffixes():
    '''
    '''
    distinct_suffix_groups = get_distinct_suffix_groups()
    distinct_suffix_groups = [list(x) for x in distinct_suffix_groups]
    distinct_suffix_groups = itertools.chain.from_iterable(distinct_suffix_groups)
    distinct_suffixes = sorted(list(set(distinct_suffix_groups)))
    return distinct_suffixes  
        


if __name__ == '__main__':

    import argparse
    import sys
    import ast
    import pprint

    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the get_all_entries_with_suffixes function
    get_all_entries_with_suffixes_parser = \
    subparsers.add_parser('get_all_entries_with_suffixes')
    get_all_entries_with_suffixes_parser.set_defaults\
    (function = get_all_entries_with_suffixes)

    # create the parser for the get_distinct_suffixes_for_word_form function
    get_distinct_suffixes_for_word_form_parser = \
    subparsers.add_parser('get_distinct_suffixes_for_word_form')
    get_distinct_suffixes_for_word_form_parser.add_argument('-word_form')
    get_distinct_suffixes_for_word_form_parser.set_defaults\
    (function = get_distinct_suffixes_for_word_form)

    # create the parser for the assign_word_form_to_suffix_group function
    assign_word_form_to_suffix_group_parser = \
    subparsers.add_parser('assign_word_form_to_suffix_group')
    assign_word_form_to_suffix_group_parser.add_argument('-word_form')
    assign_word_form_to_suffix_group_parser.set_defaults\
    (function = assign_word_form_to_suffix_group)

    # create the parser for the get_distinct_suffix_groups function
    get_distinct_suffix_groups_parser = subparsers.add_parser('get_distinct_suffix_groups')
    get_distinct_suffix_groups_parser.set_defaults(function = get_distinct_suffix_groups)

    # create the parser for the get_distinct_suffixes function
    get_distinct_suffixes_parser = subparsers.add_parser('get_distinct_suffixes')
    get_distinct_suffixes_parser.set_defaults(function = get_distinct_suffixes)

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
