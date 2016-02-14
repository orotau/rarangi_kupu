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
import teina

Text_Chunk = namedtuple('Text_Chunk', 'text_chunk start end type')

def is_number(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True


def get_open_compounds_list(file_id):

    # the file_id is used for the list of teina

    HPK_OPEN_COMPOUNDS_FILE_NAME = "hpk_open_compounds.txt"
    OTHER_OPEN_COMPOUNDS_FILE_NAME = "other_open_compounds.txt"

    cf = config.ConfigFile()
    text_files_path = (cf.configfile[cf.computername]['text_files_path'])

    open_compounds_list = []

    hpk_open_compounds_file_path = \
    text_files_path + HPK_OPEN_COMPOUNDS_FILE_NAME
 
    other_open_compounds_file_path = \
    text_files_path + OTHER_OPEN_COMPOUNDS_FILE_NAME 

    with open(hpk_open_compounds_file_path, 'r') as f:
        for line in f:
            open_compounds_list.append(line.replace('\n', ''))

    with open(other_open_compounds_file_path, 'r') as f:
        for line in f: 
            open_compounds_list.append(line.replace('\n', ''))  

    # add any teina that are themselves open compounds
    # and have a big brother in the list of open compounds
    for big_brother, little_brothers in teina.teina[file_id]:
        if big_brother in open_compounds_list:
            for little_brother in little_brothers:
                if ' ' in little_brother:                    
                    open_compounds_list.append(little_brother)
        else:
            # big brother not in the list of open compounds
            if ' ' in big_brother:
                print("Must add " + big_brother + " to open compounds")
                return False
            else:
                # not an open compound but it could have open compound teina
                for little_brother in little_brothers:
                    if ' ' in little_brother:                    
                        open_compounds_list.append(little_brother)                 

    # sort the list by length (longest at start)
    # to avoid say finding 'the banana' and never finding
    # 'longer version of the banana'

    open_compounds_list.sort(key=len, reverse=True)

    return open_compounds_list


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
    f) c) is refined to leave alone a name like T. W. Downes

    'Te' or 'Ngā' are excluded

    returns the decapitalised text_chunk
    '''

    excluded_words = ["Te", "Ngā"]
    text_chunk_to_return = list(text_chunk) # convert to list to allow updating

    regex_string = maori_regex.capitalised_non_compound_word

    is_any_match = re.search(regex_string, text_chunk, re.VERBOSE) # look for at least 1

    if is_any_match:
        cncc_words = re.finditer(regex_string, text_chunk, re.VERBOSE)
        for each_match in cncc_words:
            if each_match.group() not in excluded_words:
                # print(each_match.group())
                if each_match.start() == 0:
                    # first word in text_chunk
                    text_chunk_to_return[0] = text_chunk[0].lower()
                else:
                    # not the first word in text chunk
                    # check to the left
                    text_chunk_to_left = (''.join(text_chunk_to_return)
                                                 [0:each_match.start()])

                    # print("text to left", text_chunk_to_left)

                    # search this text for 'sentence boundaries'
                    for x in maori_regex.sentence_boundaries:
                        sentence_boundaries = re.finditer(x, \
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
                                break
                            else:
                                #there is no sentence boundary immediately
                                #preceding the match, keep looping
                                pass
                        else:
                            # no sentence boundaries found at all
                            pass

    else:
        # the text chunk does not contain any
        # capitalised non-closed compound words
        pass

    text_chunk_to_return = ''.join(text_chunk_to_return)
    
    return text_chunk_to_return   
        

def create_Text_Chunk(existing_Text_Chunks, text_chunk, chunk_start, chunk_end, chunk_type):

    '''
    This function takes as input
    A list of the existng Text Chunks (if any) for this line
    The 'text chunk'
    It's start position in the line
    It's end position in the line
    The type

    The function looks at the list of existing_Text_Chunks to see if
    there is room for the new text_chunk.

    There are 3 possibilities
    a) The start and end of the text_chunk lie completely inside an existing
       text chunk, in which case we return 'False'
    b) The start and end of the text_chunk lie completely outside any existing
       text chunks, in which case we create a new Text Chunk and return it
    c) The text_chunk overlaps one or more existing Text Chunks in which case
       we return 'Error', almost certainly some error in the logic
    '''

    if existing_Text_Chunks == []:
        is_inside = False
        is_outside = True
    else:
        # check if the prospective text_chunk is TOTALLY inside ANY existing
        # only need to find one
        is_inside = False
        for etc in existing_Text_Chunks:
            if etc.start <= chunk_start and etc.end >= chunk_end:
                is_inside = True
                break

        if not is_inside:
            # check if the prospective text_chunk is TOTALLY outside ALL existing
            is_outside = True
            for etc in existing_Text_Chunks:
                if chunk_end <= etc.start or chunk_start >= etc.end:
                    # it is outside
                    pass # keep checking
                else:
                    is_outside = False
                    break
    
    if is_inside:
        return False

    elif is_outside:
        #  create the chunk
        text_chunk_to_return = Text_Chunk(text_chunk,
                                          chunk_start,
                                          chunk_end,
                                          chunk_type)
        return text_chunk_to_return

    else:
        # there is overlap
        raise NameError('Overlap Found')
    

                    
def process_text_file(file_id):

    TEXT_EXTENSION = "txt"

    cf = config.ConfigFile()
    text_files_path = (cf.configfile[cf.computername]['text_files_path'])
    text_file_path = text_files_path + file_id + os.extsep + TEXT_EXTENSION

    # get the open compounds list to use to search for
    ocs = get_open_compounds_list(file_id)

    chunked_lines = {}

    with open(text_file_path, 'r') as f:
        for line_number_minus_one, line in enumerate(f):
            line_number = line_number_minus_one + 1
            # if line_number > 3: break
            line_to_chunk = decapitalise(line)
            # print(line_to_chunk)
            
            #initialise dictionary
            chunked_lines[line_number] = []

            '''

            #Group 1 - Open Compounds
            CHUNK_TYPE = "oc"
            for oc in ocs:
                oc_matches = re.finditer(r'\b' + oc + r'\b', line_to_chunk)
                for oc_match in oc_matches:
                    print(line_number, oc_match)
                    try:
                        return_from_create_Text_Chunk = \
                            create_Text_Chunk(chunked_lines[line_number],
                            oc_match.group(),
                            oc_match.start(),
                            oc_match.end(),
                            CHUNK_TYPE)
                    except NameError:
                        print("something has gone wrong")
                    else:
                        if return_from_create_Text_Chunk:
                            print(return_from_create_Text_Chunk)
                            chunked_lines[line_number].append(
                            return_from_create_Text_Chunk)
                        else:
                            print("all inside")

            #Group 2 - Vanilla Open Compounds
            CHUNK_TYPE = "voc"
            regex_string = maori_regex.sequential_capitalised_words
            voc_matches = re.finditer(regex_string, line_to_chunk, re.VERBOSE)
            for voc_match in voc_matches:
                print(line_number, voc_match)
                try:
                    return_from_create_Text_Chunk = \
                        create_Text_Chunk(chunked_lines[line_number],
                        voc_match.group(),
                        voc_match.start(),
                        voc_match.end(),
                        CHUNK_TYPE)
                except NameError:
                    print("something MAY have gone wrong")
                else:
                    if return_from_create_Text_Chunk:
                        print(return_from_create_Text_Chunk)
                        chunked_lines[line_number].append(
                        return_from_create_Text_Chunk)
                    else:
                        print("all inside")

            #Group 3 - Mixed Open Compounds
            CHUNK_TYPE = "moc"
            regex_string = maori_regex.mixed_open_compound
            moc_matches = re.finditer(regex_string, line_to_chunk, re.VERBOSE)
            for moc_match in moc_matches:
                print(line_number, moc_match)
                try:
                    return_from_create_Text_Chunk = \
                        create_Text_Chunk(chunked_lines[line_number],
                        moc_match.group(),
                        moc_match.start(),
                        moc_match.end(),
                        CHUNK_TYPE)
                except NameError:
                    print("something MAY have gone wrong")
                else:
                    if return_from_create_Text_Chunk:
                        print(return_from_create_Text_Chunk)
                        chunked_lines[line_number].append(
                        return_from_create_Text_Chunk)
                    else:
                        print("all inside")

            #Group 4 - Isolated Capitalised Non-Compound Word
            # The regex will find all Capitalised Non-Compound Words
            # but if they are contained in Compound Words previously found
            # they will be rejected (classed as "all inside")
            # resulting in isolated.
            CHUNK_TYPE = "icncw"
            regex_string = maori_regex.capitalised_non_compound_word
            icncw_matches = re.finditer(regex_string, line_to_chunk, re.VERBOSE)
            for icncw_match in icncw_matches:
                print(line_number, icncw_match)
                try:
                    return_from_create_Text_Chunk = \
                        create_Text_Chunk(chunked_lines[line_number],
                        icncw_match.group(),
                        icncw_match.start(),
                        icncw_match.end(),
                        CHUNK_TYPE)
                except NameError:
                    print("something MAY have gone wrong")
                else:
                    if return_from_create_Text_Chunk:
                        print(return_from_create_Text_Chunk)
                        chunked_lines[line_number].append(
                        return_from_create_Text_Chunk)
                    else:
                        print("all inside")


            #Group 5 - Isolated Closed-Compound Words
            # The regex will find all Closed-Compound Words
            # but if they are contained in Mixed Open Compound Words previously found
            # they will be rejected (classed as "all inside")
            # resulting in isolated.
            CHUNK_TYPE = "iccw"
            regex_string = maori_regex.isolated_closed_compound_word
            iccw_matches = re.finditer(regex_string, line_to_chunk, re.VERBOSE)
            for iccw_match in iccw_matches:
                print(line_number, iccw_match)
                try:
                    return_from_create_Text_Chunk = \
                        create_Text_Chunk(chunked_lines[line_number],
                        iccw_match.group(),
                        iccw_match.start(),
                        iccw_match.end(),
                        CHUNK_TYPE)
                except NameError:
                    print("something MAY have gone wrong")
                else:
                    if return_from_create_Text_Chunk:
                        print(return_from_create_Text_Chunk)
                        chunked_lines[line_number].append(
                        return_from_create_Text_Chunk)
                    else:
                        print("all inside")
        
                                          
                                         
            #Group 6 - Isolated Lower Case Non-Compound Word
            # The regex will find all Lower Case Non-Compound Words
            # but if they are contained in Compound Words previously found
            # they will be rejected (classed as "all inside")
            # resulting in isolated.
            CHUNK_TYPE = "ilcncw"
            regex_string = maori_regex.lower_case_non_compound_word
            ilcncw_matches = re.finditer(regex_string, line_to_chunk, re.VERBOSE)
            for ilcncw_match in ilcncw_matches:
                print(line_number, ilcncw_match)
                try:
                    return_from_create_Text_Chunk = \
                        create_Text_Chunk(chunked_lines[line_number],
                        ilcncw_match.group(),
                        ilcncw_match.start(),
                        ilcncw_match.end(),
                        CHUNK_TYPE)
                except NameError:
                    print("something MAY have gone wrong")
                else:
                    if return_from_create_Text_Chunk:
                        print(return_from_create_Text_Chunk)
                        chunked_lines[line_number].append(
                        return_from_create_Text_Chunk)
                    else:
                        print("all inside")      

            #Group 7 - Punctuation and Whitepace
            CHUNK_TYPE = "paws"
            paws_matches = re.finditer(r'\W+', line_to_chunk)
            for paws_match in paws_matches:
                print(line_number, paws_match)
                try:
                    return_from_create_Text_Chunk = \
                        create_Text_Chunk(chunked_lines[line_number],
                        paws_match.group(),
                        paws_match.start(),
                        paws_match.end(),
                        CHUNK_TYPE)
                except NameError:
                    print("something has gone wrong")
                else:
                    if return_from_create_Text_Chunk:
                        print(return_from_create_Text_Chunk)
                        chunked_lines[line_number].append(
                        return_from_create_Text_Chunk)
                    else:
                        print("all inside")   

            '''   

            #Group 8 - Everything Else
            CHUNK_TYPE = "misc"
            regex_string = maori_regex.misc
            misc_matches = re.finditer(regex_string, line_to_chunk, re.VERBOSE)
            for misc_match in misc_matches:
                print(line_number, misc_match)
                try:
                    return_from_create_Text_Chunk = \
                        create_Text_Chunk(chunked_lines[line_number],
                        misc_match.group(),
                        misc_match.start(),
                        misc_match.end(),
                        CHUNK_TYPE)
                except NameError:
                    print("something HAS gone wrong")
                else:
                    if return_from_create_Text_Chunk:
                        # print(return_from_create_Text_Chunk)
                        chunked_lines[line_number].append(
                        return_from_create_Text_Chunk)
                    else:
                        print("all inside")      


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
