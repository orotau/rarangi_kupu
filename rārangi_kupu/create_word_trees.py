from bs4 import BeautifulSoup, Tag
from collections import namedtuple
import config
import os
import pprint

def create_word_trees(letter):
    '''
    We are using the concept of a 'word tree' to represent each 'word'

    Each 'word tree' will be stored as a Python dictionary

    The unique key consists of 4 parts:
    1. root - A digit
    2. trunk - A word form such as 'hua'
    3. branch - A digit
    4. twig - null (will be a digit for 'sub entries')

    The 'word trees' will be saved as a json file (because its
    human readable). 
    '''

    #create named tuple to store unique keys
    Word_ID = namedtuple('Word_ID', 'root trunk branch twig')

    # get the dump path
    cf = config.ConfigFile()
    dump_folder = (cf.configfile[cf.computername]['dump_path'])
    target_folder = dump_folder + letter + "/"

    #get all the files in the target folder
    html_file_names = os.listdir(target_folder)

    #open the html files for the letter
    for fyle in html_file_names:
        with open(target_folder + fyle) as f: #read only
            soup = BeautifulSoup(f.read())

        #get all the headword tags in the html document
        all_headword_tags = soup.find_all(class_="headword")

        #narrow down to the headword that matches the html document name
        headword = fyle.split('.')[0] #get rid of the .html file extension
        headword_tags = [x for x in all_headword_tags if x.string==headword]
        pprint.pprint(headword_tags) #debug

        #We are *assuming* that the headword tags are ordered correctly
        #We may have to revisit this later

        for counter, headword_tag in enumerate(headword_tags):
            #get all the raw branches and twigs (if there are any) for each headword_tag
            #At this stage a raw branch / twig contains all the information we need
            #but in a form that needs alot of processing
            all_raw_branches_and_twigs = get_raw_branches_and_twigs(soup, headword_tag)

            print('Headword', counter + 1)
            print('# Branches and Twigs', len(all_raw_branches_and_twigs))
            for raw_branch_or_twig in all_raw_branches_and_twigs:
                print ("++++++++++++FINAL++++++++++++++")
                print (str(raw_branch_or_twig)[:])
                print ("++++++++++++FINAL++++++++++++++")
                #process branch or twig

        
        

def get_raw_branches_and_twigs(soup, headword_tag):
    '''
    Given the headword tag
    returns a list of all of its 'raw branches'
    '''
    raw_branches_and_twigs = []
    ns = headword_tag.parent

    while True:
        ns = ns.next_sibling
        if isinstance(ns, Tag):
            mini_soup = BeautifulSoup(str(ns))
            print('*****processing********')
            print (mini_soup)
            print('*****processing********')
            #Have we gone too far?
            too_far = False
            if not mini_soup.find(class_="variantno") is None:
                #we have found the next variantno in our mini_soup
                too_far = True 
            if not mini_soup.find(class_="headword") is None:
                #we have found the next headword in our mini_soup
                too_far = True
            if (mini_soup.p and mini_soup.get_text() == '\n' and
                len(list(mini_soup.descendants)) == 2):
                #we have found a <p></p>   assming at end of document
                too_far = True           
            #other 'too far' checks here             

            if too_far:
                break #exit loop
            else:
                raw_branches_and_twigs.append(ns)

        else:
            #keep looping, we don't have a Tag
            pass

    return raw_branches_and_twigs

def is_twig(raw_branch_or_twig):
    if raw_branch_or_twig.find(class_="subentry") is None:
        return False
    else:
        return True


if __name__ == '__main__':
    import pū
    import sys
    try:
        first_argument = sys.argv[1]
    except IndexError:
        #No argument given
        print ("Please supply a Māori letter as the argument")
        sys.exit()

    if first_argument in pū.all_letters:
        create_word_trees(first_argument)
        print ('Done - thanks')
    elif first_argument == 'test':
        create_word_trees("test")
    else:
        print ("The first argument must be a Māori letter")
        sys.exit()
