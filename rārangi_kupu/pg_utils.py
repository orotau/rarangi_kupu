'''
populate the Postgresql table
with the words
'''
import psycopg2
import keyring
#import cherrypy
import json
import xlrd
import config
import post_process_text_file
from collections import namedtuple

Text_Chunk = namedtuple('Text_Chunk', 'text_chunk start end type')

def get_db_access_info():
    cf = config.ConfigFile()
    db_name = cf.configfile[cf.computername]['database']
    db_user = cf.configfile[cf.computername]['user']
    db_password = keyring.get_password(cf.configfile[cf.computername]
                                               ['id'], db_user)

    return db_name, db_user, db_password


def populate_pgt_word():

    # get the word list
    cf = config.ConfigFile()
    iwa_path = (cf.configfile[cf.computername]['iwa_path'])
    json_filename = "all_words_for_iwa.json"
    full_json_path = iwa_path + json_filename
    with open(full_json_path, 'r') as f:
        unique_word_forms = json.load(f)

        db_access_info = get_db_access_info()
        with psycopg2.connect(database=db_access_info[0],
                              user=db_access_info[1],
                              password=db_access_info[2]) as connection:

            with connection.cursor() as cursor:
                for w in unique_word_forms:
                    cursor.execute("INSERT INTO pgt_word VALUES (%s)", (w,))


def populate_pgt_board_children():

    # get the data for the 3 columns
    cf = config.ConfigFile()
    iwa_path = (cf.configfile[cf.computername]['iwa_path'])
    xl_filename = "children-counts.xlsx"
    full_xl_path = iwa_path + xl_filename
    wb = xlrd.open_workbook(full_xl_path)
    sheet = wb.sheet_by_index(0)  # first sheet

    words = sheet.col_values(0, 1)  # column 1, row 2
    centre_letters = sheet.col_values(1, 1)   # column 2, row 2
    children_counts = sheet.col_values(2, 1)  # column 3, row 2

    db_access_info = get_db_access_info()
    with psycopg2.connect(database=db_access_info[0],
                          user=db_access_info[1],
                          password=db_access_info[2]) as connection:

        with connection.cursor() as cursor:
            for x, y, z in zip(words, centre_letters, children_counts):
                cursor.execute("INSERT INTO pgt_board_children VALUES (%s, %s, %s)", (x, y, z))


def populate_word_frequency():

    TAUIRA_FILE_ID = "hpk_tauira"

    # get the data
    words_and_frequency = post_process_text_file.get_words_and_counts(TAUIRA_FILE_ID)
    db_access_info = get_db_access_info()
    with psycopg2.connect(database=db_access_info[0],
                          user=db_access_info[1],
                          password=db_access_info[2]) as connection:

        with connection.cursor() as cursor:
            for x, y in words_and_frequency:
                cursor.execute("INSERT INTO pgt_word_frequency VALUES (%s, %s)", (x, y))


if __name__ == '__main__':

    import sys
    import argparse
    import ast

    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the populate_pgt_word function
    populate_pgt_word_parser = subparsers.add_parser('populate_pgt_word')
    populate_pgt_word_parser.set_defaults(function=populate_pgt_word)

    # create the parser for the populate_pgt_board_children function
    populate_pgt_board_children_parser = subparsers.add_parser('populate_pgt_board_children')
    populate_pgt_board_children_parser.set_defaults(function=populate_pgt_board_children)

    # create the parser for the populate_word_frequency function
    populate_word_frequency_parser = subparsers.add_parser('populate_word_frequency')
    populate_word_frequency_parser.set_defaults(function=populate_word_frequency)

    # parse the arguments
    arguments = parser.parse_args()
    arguments = vars(arguments)  # convert from Namespace to dict

    # attempt to extract and then remove the function entry
    try:
        function_to_call = arguments['function']
    except KeyError:
        print("You need a function name. Please type -h to get help")
        sys.exit()
    else:
        # remove the function entry
        del arguments['function']

    if arguments:
        # remove any entries that have a value of 'None'
        # We are *assuming* that these are optional
        # We are doing this because we want the function definition to define
        # the defaults (NOT the function call)
        arguments = {k: v for k, v in arguments.items() if v is not None}

        # alter any string 'True' or 'False' to bools
        arguments = {k: ast.literal_eval(v) if v in ['True', 'False'] else v
                     for k, v in arguments.items()}

    result = function_to_call(**arguments)
    # note **arguments works fine for empty dict {}
