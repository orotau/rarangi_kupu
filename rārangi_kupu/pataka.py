'''
The module to access the json files
I'm not really sure what it does as yet
'''

import config
import json
import ast
from collections import namedtuple
import pū
import maoriword as mw

class HPK():
    
    def __init__(self):

        Word_ID = namedtuple('Word_ID', 'root_number trunk branch_number twig twig_number')
        
        #gather all the parts and make one large dictionary
        hpk = {}

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
            setattr(self, letter, word_trees_from_json)
            hpk.update(word_trees_from_json)

        self.hpk = hpk

    def get_headwords(self, letter='all'):
        '''
        the purpose of this method is to get all the headwords
        from HPK. Given a letter it will return all the headwords
        for that letter. Otherwise will return all of them.

        They will be returned as a tuple of tuples
        
        A headword is a unique 'root number, trunk' combination
        '''

        if letter == 'all':
            word_trees_temp = self.hpk
        else:
            word_trees_temp = getattr(self, letter)

        headwords_bloop = ((k.root_number, k.trunk) for k in word_trees_temp.keys())
        return set(headwords_bloop)        

if __name__ == '__main__':
    word_trees = HPK()

