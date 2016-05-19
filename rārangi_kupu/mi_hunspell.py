'''
The module to help create the dic and aff files for hunspell 
'''

import pataka

def get_suffix_groups():
    '''
    The purpose of this function is to get every entry
    in HPK that has a suffix.

    There is no distinction between passive suffixes and
    nominalisation suffixes (at least at this stage)
    '''

    passives = pataka.get_passives(False)
    nominalisations = pataka.get_nominalisations(False)

    print(passives)
    print(nominalisations)

if __name__ == '__main__':

    import argparse
    import sys
    import ast

    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the get_all_entries function
    get_all_entries_parser = subparsers.add_parser('get_suffix_groups')
    get_all_entries_parser.set_defaults(function = get_suffix_groups)

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
