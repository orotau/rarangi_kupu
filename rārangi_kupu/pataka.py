'''
The module to access the json files
I'm not really sure what it does as yet
'''

import config
import json
import ast
from collections import namedtuple
import pū

class HPK():
    
    def __init__(self):

        Word_ID = namedtuple('Word_ID', 'root_number trunk branch_number twig twig_number')
        
        #unpickle all the parts and make one large dictionary
        cf = config.ConfigFile()
        json_path = (cf.configfile[cf.computername]['json_path'])

        for letter in pū.dictionary_letters:
            print ('gathering json', letter)
            json_filename = letter + ".json"
            full_json_path = json_path + json_filename
            with open(full_json_path,'r') as f:
                word_trees_from_json = json.load(f)

            #round trip
            word_trees_from_json = {Word_ID(**ast.literal_eval(k)):v for k,v in word_trees_from_json.items()}

if __name__ == '__main__':
    HPK()
