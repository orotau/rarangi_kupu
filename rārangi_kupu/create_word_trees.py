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

    temp_dict = {}

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

        for root_counter, headword_tag in enumerate(headword_tags):
            #get all the raw branches and twigs (if there are any) for each headword_tag
            #At this stage a raw branch / twig contains all the information we need
            #but in a form that needs alot of processing
            all_raw_branches_and_twigs = get_raw_branches_and_twigs(soup, headword_tag)

            print('Headword', root_counter + 1)
            print('# Branches and Twigs', len(all_raw_branches_and_twigs))
            for raw_branch_or_twig in all_raw_branches_and_twigs:
                print ("++++++++++++FINAL++++++++++++++")
                #print (str(raw_branch_or_twig)[:])
                print ("++++++++++++FINAL++++++++++++++")
                #populate the dictionary key for each word tree
                root = root_counter + 1

                #trunk, branch and twig
                branch_number = get_branch_number(raw_branch_or_twig)
                if not branch_number is None:
                    #we have a branch
                    trunk = headword
                    branch = branch_number
                    twig = False

                    #we need to have available the branch number for the twig
                    #We are assuming that the first time through we must have a branch
                    #serves as a check of that (I think)
                    branch_number_for_twig = branch_number
                else:
                    #we have a twig
                    trunk = raw_branch_or_twig.find(class_="subentry").string
                    branch = branch_number_for_twig
                    twig = True #assuming there can only ever be one twig per branch
 
                word_id = Word_ID(root, trunk, branch, twig)

                leaves = {}
                atua = get_atua(raw_branch_or_twig)
                #temp_dict[word_id] = 'banana'
        #pprint.pprint (temp_dict)

    

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
            #print (mini_soup)
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
                #we have found a <p></p>   assuming at end of document
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


def get_branch_number(raw_branch_or_twig):
    '''
    this function examines the raw_branch_or_twig passed
    returns the branch number if a branch
    returns None if it is a twig

    Quality control on the 'raw_branch_or_twig' passed 
    raises a NameError if neither branch or twig
    raises assert errors if any of
    2 or more branches mixed, 
    2 or more twigs mixed
    branches and twigs mixed
    '''

    #do we have a branch or a twig or a problem!
    is_branch = False #initialise
    is_twig = False #initialise 
    branch_or_twig = raw_branch_or_twig.find(class_="majsense")  
    if not branch_or_twig is None:
        #we have found at least one branch
        assert raw_branch_or_twig.find(class_="subentry") is None, \
               "We have found a twig mixed in with a branch"
        assert len(raw_branch_or_twig.find_all(class_="majsense")) == 1, \
               "More than 1 branch found where there must only be 1"
        is_branch = True
    else:
        #Not a branch! Is it a twig?
        branch_or_twig = raw_branch_or_twig.find(class_="subentry")
        if not branch_or_twig is None:
            #We have found at least one twig
            assert len(raw_branch_or_twig.find_all(class_="subentry")) == 1, \
                   "More than 1 twig found where there must only be 1"
            is_twig = True
        else:
            #Neither branch nor twig!
            raise NameError('Neither branch nor twig found')        
    
    if is_branch:
        branch = branch_or_twig    
        if not branch.string:
            #empty string (1 and only 1 branch)
            #not hugely happy with this as branch.string could possibly? be None for other reasons
            branch_number = 1
        else:    
            branch_number = branch.string.replace(".","").strip() #We have '  2.  ' for example
            branch_number = int(branch_number)
        return branch_number

    if is_twig:
        return None

def get_atua:
    pass


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
