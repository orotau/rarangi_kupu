'''
This module establishes is used to introduce a 'difficulty level'
for each board, as follows

a) First get a frequency score for each child word
for a board where a board is defined by '9 letter word" + "compulary letter"
'''    

# excluding those 9 letter words with
# 3 digraphs because they yield hardly
# any children and are a bit messy to
# put in the grid

import config
import psycopg2
import maoriword as mw
import pprint
import json
import pangakupu as pk
import boards_and_children
import pg_utils

def get_word_frequency_distribution():
    '''
    For each word, middle letter combination 
    split the data into groups
    '''

    # get the word frequency data
    db_access_info = pg_utils.get_db_access_info()
    with psycopg2.connect(database=db_access_info[0],
                          user=db_access_info[1],
                          password=db_access_info[2]) as connection:

        with connection.cursor() as cursor:
            word_frequency_pairs = []

            all_word_frequency_data_query = \
                ' '.join((
                    "SELECT * FROM pgt_word_frequency",
                ))

            cursor.execute(all_word_frequency_data_query)
            word_frequency_pairs = cursor.fetchall()  # list of tuples
            words = [x[0] for x in word_frequency_pairs]

    scores = {}
    for k, v in boards_and_children.boards_and_children.items():
        child_word_frequencies = []
        for child_word in v:
            try:
                child_word_index = words.index(child_word)
            except ValueError:
                # the headword in the dictionary doesn't appear
                # anywhere in the example text
                child_word_score = 0
            else:
                child_word_score = word_frequency_pairs[child_word_index][1]

            child_word_frequencies.append(child_word_score)

        scores[k] = sorted(child_word_frequencies)

        intervals = [frozenset(range(24, 100000)), \
                     frozenset(range(6, 24)), \
                     frozenset(range(6))]
        counts = [0] * len(intervals)

        for n in sorted(child_word_frequencies):
          for i, inter in enumerate(intervals):
            if n in inter:
              counts[i] += 1

        if not(counts[0] <= 5 or sum(counts) < 10):
            if counts[2] >= 4:
                print(k, counts[0], counts[0] + counts[1], sum(counts))
        

    



if __name__ == '__main__':

    import sys
    import argparse
    import ast

    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the get_average_score function
    get_word_frequency_distribution_parser = subparsers.add_parser \
    ('get_word_frequency_distribution')
    get_word_frequency_distribution_parser.set_defaults \
    (function = get_word_frequency_distribution)

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

