'''
The purpose of this module is to create text files
for word frequency analysis.

Each file will have a name to allow it to be referenced

Before the file is created an existing version will be checked for
If it is found then the user will be asked if they wish to overwrite

There will be specific issues that arise for each file (such as spelling errors)
'''
import config
import os
import pataka
import maoriword as mw
import spelling_mistakes
import mi_hunspell

def query_yes_no(question, default="no"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def create_text_file(file_id):
    #create a text file with the name file_id.TEXT_EXTENSION
    #returns None if the text file exists and the user decides to cancel

    TEXT_EXTENSION = "txt"
    TAUIRA_FILE_ID = "hpk_tauira" # duplicated with the choices in the call
    DEFINITIONS_FILE_ID = "hpk_definitions"
    HPK_OPEN_COMPOUNDS_FILE_ID = "hpk_open_compounds"
    HUNSPELL_DIC_CANDIDATES_FILE_ID = "mi_dic_candidates"
    HUNSPELL_DIC_SUFFIXES_FILE_ID = "mi_dic_suffixes"
    HPK_ALL_WORDS = "hpk_all"

    cf = config.ConfigFile()
    text_files_path = (cf.configfile[cf.computername]['text_files_path'])
    text_file_path = text_files_path + file_id + os.extsep + TEXT_EXTENSION
    if os.path.isfile(text_file_path):
        # file exists, check to see if it should be overridden
        file_exists = True
        overwrite_file = query_yes_no("Do you want to OVERWRITE the existing file?")
    else:
        file_exists = False

    if file_exists and not overwrite_file:
        print("Existing file left as is")
        return None

    if file_exists and overwrite_file:
        # delete existing file
        os.remove(text_file_path)

    #time to create the file
    if file_id == TAUIRA_FILE_ID:
        all_tauira = []
        all_entries = pataka.get_all_entries() 

        # we are only interested in those entries that have at least one tauira
        all_entries_with_tauira = {k:v for k,v in all_entries.items() if v["tauira"]}

        # extract each tauira into a single long list
        for k, v in all_entries_with_tauira.items():
            for t in v["tauira"]:
                all_tauira.extend([t]) # note [] round the t to prevent 't' 'h' 'i' 's'
        
        # replace any stray "\n" with a space ' '       
        all_tauira = [t.replace("\n", " ") for t in all_tauira]

        # fix up any spelling mistakes
        for index, t in enumerate(all_tauira):
            for sm in spelling_mistakes.spelling_mistakes[TAUIRA_FILE_ID]:
                if sm[0] in t:
                    all_tauira[index] = t.replace(sm[0], sm[1])

        #get rid of dups and  do Pākehā style sorting as maori code not working Feb 2016
        all_tauira = sorted(list(set(all_tauira)))

        for t in all_tauira:
            insides = [x for x in all_tauira if t in x and t != x]
            if insides:
                print (t)
                for i in insides:
                    print (i)
                print ("===========================")
                print ("")

        # write the file
        with open(text_file_path, "a") as myfile:
            for t in all_tauira:
                myfile.write(t + "\n")

        return True

    if file_id == DEFINITIONS_FILE_ID:
        all_definitions = []
        all_entries = pataka.get_all_entries() 

        # we are only interested in those entries that have at least one tauira
        all_entries_with_definitions = ({k:v for k,v in all_entries.items() 
                                       if v["whakamāoritanga"]})

        # extract each DEFINITION into a single long list
        for k, v in all_entries_with_definitions.items():
            all_definitions.extend([v["whakamāoritanga"]]) 
        
        # replace any stray "\n" with a space ' '       
        all_definitions = [d.replace("\n", " ") for d in all_definitions]

        #get rid of dups and  do Pākehā style sorting as maori code not working Feb 2016
        all_definitions = sorted(list(set(all_definitions)))

        # write the file
        with open(text_file_path, "a") as myfile:
            for t in all_definitions:
                myfile.write(t + "\n")

        return True



    if file_id == HPK_OPEN_COMPOUNDS_FILE_ID:
        all_word_forms = pataka.get_word_forms(p = False, n = False)

        # write the file
        with open(text_file_path, "a") as myfile:
            for candidate_word in all_word_forms['ese'].not_ok:
                if " " in candidate_word:
                    # remove non-compound words
                    compound_word = candidate_word                    
                    myfile.write(compound_word + "\n")
        return True


    if file_id == HUNSPELL_DIC_CANDIDATES_FILE_ID:
        dic_candidates = pataka.get_all_entries_as_list()

        # write the file
        with open(text_file_path, "a") as myfile:
            for candidate_word in dic_candidates:
                myfile.write(candidate_word + "\n")
        return True


    if file_id == HUNSPELL_DIC_SUFFIXES_FILE_ID:
        # trying just pprinting the dict
        dic_suffixes = mi_hunspell.get_distinct_suffixes_for_word_form()

        from pprint import pprint

        # write the file
        with open(text_file_path, "a") as myfile:
            myfile.write("words_and_suffixes = (" + "\n")
            pprint(dic_suffixes, stream=myfile)
            myfile.write(")" + "\n")
        return True  

    if file_id == HPK_ALL_WORDS:
        from collections import namedtuple
        Word_Forms = namedtuple('Word_Forms', 'ok not_ok')  
        word_forms = pataka.get_word_forms()
        word_forms_as_list = (word_forms['ese'].ok + word_forms['ese'].not_ok +
                                  word_forms['n'].ok + word_forms['n'].not_ok +   
                                  word_forms['p'].ok + word_forms['p'].not_ok)
        word_forms_as_list = list(set(word_forms_as_list))
        word_forms_as_list.sort(key=mw.get_list_sort_key)
        # write the file
        with open(text_file_path, "a") as myfile:
            for word_form in word_forms_as_list:
                myfile.write(word_form + "\n")
        return True
        

if __name__ == '__main__':

    import sys
    import argparse
    import ast

    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the get_all_entries function
    create_text_file_parser = subparsers.add_parser('create_text_file')
    create_text_file_parser.add_argument('file_id', choices = ['hpk_tauira',
                                                               'hpk_definitions', 
                                                               'hpk_open_compounds',
                                                               'mi_dic_candidates',
                                                               'hpk_all',                                                               'mi_dic_candidates',
                                                               'mi_dic_suffixes'])
    create_text_file_parser.set_defaults(function = create_text_file)

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
