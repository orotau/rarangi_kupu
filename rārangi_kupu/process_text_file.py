'''
The purpose of this module is to process the text files
created by create_text_file.py

This is for the purposes of word frequency analysis
'''

import config
import os
import re

def process_text_file(file_id):

    TEXT_EXTENSION = "txt"
    TAUIRA_FILE_ID = "hpk_tauira" # duplicated with the choices in the call

    cf = config.ConfigFile()
    text_files_path = (cf.configfile[cf.computername]['text_files_path'])
    text_file_path = text_files_path + file_id + os.extsep + TEXT_EXTENSION

    # Get the non-compound maori words using regex
    regex_maori_word = r"""
    \b                      # capture whole words only

    (?:

    (?:                     # group so we can use the +
                            # non-capturing so the whole word is returned
    ng|                     # needs to be before the n
    wh|                     # needs to be before the w and h
    [hkmnprtw]
    )
    ?                       # 0 or 1 times
    
    (?:
    [aeiouāēīōū]
    )
    
    )                      
    +                       # one or more of the above
    \b
    """

    regex_open_compound_candidate = r"""

    (?:
    [A-ZĀĒĪŌŪ]              # capital letter to start
    [a-zāēīōū]+             # one or more alphanumeric characters
    \s+                     # one or more spaces
    )
    +                       # one or more

    (?:
    \b
    [A-ZĀĒĪŌŪ]              # capital letter to start
    [a-zāēīōū]+             # one or more alphanumeric characters
    \b
    )

    (?!
    -                       # Don't bump into a closed compound
    )

    """

    regex_closed_compound = r"""

    (?:    

    (?:
    \w+                     # one word 
    )

    (?:  
    -                       # dash
    \w+                     # one word
    )+                      # one or more times

    )
    """

    regex_capitalised_word = r"""

    (?:
                     
    (?:
    \b
    [AEIOUĀĒĪŌŪHKMNPRTW]    #capital letter to start
    \w+                     #one or more alphanumeric characters
    \b
    )

    )
    """




    test = "Waiho te mīti kia āta hū i roto i te hōpane mō tētahi 30 meneti atu anō."

    with open(text_file_path, 'r') as f:
        for line_number, line in enumerate(f):
            maori_words = re.findall(regex_maori_word, line, re.VERBOSE | re.IGNORECASE)
            all_words = re.findall(r"\w+", line)
            open_compound_candidates = re.findall(regex_open_compound_candidate, \
                                                  line, re.VERBOSE)

            closed_compounds = re.findall(regex_closed_compound, \
                                                  line, re.VERBOSE)

            capitalised_words = re.findall(regex_capitalised_word, \
                                                  line, re.VERBOSE)
                                                    
            '''
            if maori_words != all_words:
                for word in all_words:
                    if word not in maori_words:
                        if word == "whakpaipai":
                            print(all_words)
            '''
            for open_compound_candidate in open_compound_candidates:
                print("start")
                print(line_number, line)
                print(open_compound_candidate)
                print("end")
                print("\n\n")

            #for closed_compound in closed_compounds:
            #    print(closed_compound)

if __name__ == '__main__':

    import sys
    import argparse
    import ast

    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the get_all_entries function
    process_text_file_parser = subparsers.add_parser('process_text_file', help = '>>>>>> No arguments')
    process_text_file_parser.add_argument('file_id', choices = ['hpk_tauira',])
    process_text_file_parser.set_defaults(function = process_text_file)

    # parse the arguments
    arguments = parser.parse_args()
    arguments = vars(arguments) #convert from Namespace to dict

    #attempt to extract and then remove the function entry
    try:
        function_to_call = arguments['function'] 
    except KeyError:
        print ("You need a function name. Please type -h to get help")
        sys.exit()
    else:
        #remove the function entry as we are only passing arguments
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
   
    print (result)
