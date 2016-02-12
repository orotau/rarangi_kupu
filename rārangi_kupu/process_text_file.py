'''
The purpose of this module is to process the text files
created by create_text_file.py

This is for the purposes of word frequency analysis
'''

import config
from collections import namedtuple
import os
import re
import maori_regex

chunked_lines = {}
Text_Chunk = namedtuple('Text_Chunk', 'text_chunk start end type')

def is_number(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True

def decapitalise(text_chunk):
    '''
    The purpose of this function is to take the 'text_chunk'
    and decapitalise ('This' to 'this') any word that is deemed
    to start a sentence (no others).

    A word starts a sentence if *any* of the following are true
    a) It is the first word in the text_chunk
    b) It is preceded by (1 or more spaces) (' or ") (0 1 or more spaces)
    c) It is preceded by . (1 or more spaces)
    d) It is preceded by ? (1 or more spaces)
    e) It is preceded by ! (1 or more spaces)

    'Te' or 'Ngā' are excluded

    returns the decapitalised text_chunk
    '''

    excluded_words = ["Te", "Ngā"]
    text_chunk_to_return = list(text_chunk) # convert to list to allow updating

    regex_string = maori_regex.capitalised_non_closed_compound_word

    is_any_match = re.search(regex_string, text_chunk, re.VERBOSE) # look for at least 1

    if is_any_match:
        cncc_words = re.finditer(regex_string, text_chunk, re.VERBOSE)
        for each_match in cncc_words:
            if each_match.group() not in excluded_words:
                print(each_match.group())
                if each_match.start() == 0:
                    # first word in text_chunk
                    text_chunk_to_return[0] = text_chunk[0].lower()
                else:
                    # not the first word in text chunk
                    # check to the left
                    text_chunk_to_left = (''.join(text_chunk_to_return)
                                                 [0:each_match.start()])

                    # search this text for 'sentence boundaries'
                    sentence_boundaries = re.finditer(maori_regex.sentence_boundaries, \
                                                      text_chunk_to_left, re.VERBOSE)
                    
                    # find last sentence boundary (if it exists)
                    # bit of a hack to do 2 things
                    # 1) See if there is at least 1 find
                    # 2) Get the last one (exhausting iterator)
                    # can do this because don't need anything but the last match
                    found_sentence_boundaries = False
                    for sb in sentence_boundaries:
                        found_sentence_boundaries = True
                        last_sentence_boundary = sb      

                    if found_sentence_boundaries:
                        # check the last sentence boundary and see if it is
                        # just before the capitalised non closed compound word

                        if last_sentence_boundary.end() == each_match.start():
                            text_chunk_to_return[each_match.start()] = \
                            text_chunk[each_match.start()].lower()
                        else:
                            #there is no sentence boundary immediately
                            #preceding the match, do nothing
                            pass
                    else:
                        # no sentence boundaries found at all
                        pass

    else:
        # the text chunk does not contain any
        # capitalised non-closed compound words
        pass

    text_chunk_to_return = ''.join(text_chunk_to_return)
    print (text_chunk_to_return)
    print("------------------------------")
    
    return text_chunk_to_return   
        


                    
def process_text_file(file_id):

    TEXT_EXTENSION = "txt"
    TAUIRA_FILE_ID = "hpk_tauira" # duplicated with the choices in the call

    cf = config.ConfigFile()
    text_files_path = (cf.configfile[cf.computername]['text_files_path'])
    text_file_path = text_files_path + file_id + os.extsep + TEXT_EXTENSION

    with open(text_file_path, 'r') as f:
        for line_number, line in enumerate(f):
            decapitalise(line)

            '''
            #Group 1 - HPK Open Compounds - type = "hpkoc"
            all_words = re.finditer(r"\w+", line)
            for position, each_match in enumerate(all_words):
                if position == 1 and each_match.group()[0].isupper():
                    print(line_number, line)
            '''

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
