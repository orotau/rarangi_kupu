from bs4 import BeautifulSoup, Tag, NavigableString
from collections import namedtuple
import config
import os
import pprint

#create named tuple to store unique keys
Word_ID = namedtuple('Word_ID', 'root_number trunk branch_number twig twig_number')

def create_punakupu_trees(letter):
    '''
    We are using the concept of a 'word tree part' to represent each 'word'

    Each 'word tree part' will be stored as a Python dictionary

    The 'word tree part's' unique key consists of 5 pieces:
    1. root_number - A digit, 1, 2 etc.
    2. trunk - A 'word form' such as 'hua'
    3. branch_number - A digit (can be 0, if the twig comes straight out of the trunk)
    4. twig - False if there is no twig 'word form'. Otherwise the twig 'word form'
    5. twig_number - 0 if there is no twig, the twig number otherwise
    '''

    #word trees
    word_trees={}

    # get the dump path
    cf = config.ConfigFile()
    dump_folder = (cf.configfile[cf.computername]['dump_path'])
    target_folder = dump_folder + letter + "/"

    #get all the files in the target folder (exclude backup files, ending with tilde)
    html_file_names = [f for f in os.listdir(target_folder) if not f.endswith('~')]

    #open the html files for the letter
    for fyle in html_file_names:
        with open(target_folder + fyle) as f: #read only
            soup = BeautifulSoup(f.read(), "html.parser")

        #get all the headword tags in the html document
        all_headword_tags = soup.find_all(class_="headword")

        #narrow down to the headword that matches the html document name
        headword = fyle.split('.html')[0] #get rid of the .html file extension

        trunk = headword #set the trunk
    
        headword_tags = [x for x in all_headword_tags if x.string==headword]
        #pprint.pprint(headword_tags) #debug

        #We are *assuming* that the headword tags are ordered correctly
        #We may have to revisit this later

        for root_counter, headword_tag in enumerate(headword_tags):

            root_number = root_counter + 1 #set the root_number

            branch_number_set = False #used to identify when twigs go straight on a trunk

            #get all the raw branches and twigs on the tree
            #it is possible that there can be no branches or there can be no twigs
            all_raw_branches_and_twigs = get_raw_branches_and_twigs(soup, headword_tag)

            for counter, raw_branch_or_twig in enumerate(all_raw_branches_and_twigs):
                #identify each branch and twig by setting
                #branch_number, twig, twig_number for each branch and twig on the tree

                raw_branch_or_twig_tbp = raw_branch_or_twig
                partitioned_raw_branch_or_twig = partition_raw_branch_or_twig(raw_branch_or_twig_tbp)
                pprint.pprint (partitioned_raw_branch_or_twig)
                print("=======================================")
                
                branch_number = get_branch_number(partitioned_raw_branch_or_twig[0])

                if not branch_number is None:
                    #we have a branch
                    branch_number_set = True
                    branch_number_for_twig = branch_number
                    twig = False #twig always False for a branch
                    twig_number = 0 #twig_number always 0 for a branch (*)
                else:
                    #we have a twig
                    twig = partitioned_raw_branch_or_twig[0].find(class_="subentry").string

                    #set the branch number for the twig
                    if not branch_number_set:
                        #twig directly on trunk
                        branch_number = 0
                    else:
                        branch_number = branch_number_for_twig

                    #set the twig number for the twig
                    if branch_number_set:
                        twig_number = twig_number + 1 #using (*) above
                    else:
                        #twig directly on trunk
                        if counter == 0:
                            #first time through loop
                            twig_number = 1
                        else:
                            twig_number = twig_number + 1 
 
                #hack because 'hamo' and 'hamo pango' are updside down in online version
                if twig == 'hamo pango':
                    branch_number = 1

                word_id = Word_ID(root_number, trunk, branch_number, twig, twig_number)
                print("typeee", type(word_id))

                ttt_leaves = {} # tuakana, teina, titiro
                # Tuakana
                all_tuakana = []
                for partition in partitioned_raw_branch_or_twig:
                    tuakana = get_tuakana(partition)
                    if tuakana:
                        print(tuakana)
                        all_tuakana.append(tuakana)

                if all_tuakana:
                    print(all_tuakana)
                    ttt_leaves["tuakana"] = all_tuakana[0]
                    print("dict", ttt_leaves["tuakana"])
                else:
                    print("hi")
                    ttt_leaves["tuakana"] = None

                if word_id in word_trees:
                    #major problem the key already exists!
                    #logic problem - revisit drawing board!
                    print ('key', word_id, 'already exists!')
                    if word_id.trunk == 'Pūtahi-nui-o-Rehua':
                        pass #error in HPK
                    else:
                        raise ValueError
                else:
                    word_trees[word_id] = ttt_leaves["tuakana"]

                print(word_id, "durp")

                print('-------------------------------')

    return word_trees


def get_raw_branches_and_twigs(soup, headword_tag):
    '''
    Given the headword tag returns a list of all of its 'raw branches' and 'raw twigs'
    
    <p style="margin-top: 0px; margin-bottom: 0px"> HEADWORD TAG'S PARENT
        <span class="headword">ehuehu</span> THIS IS AN EXAMPLE OF A HEADWORD TAG (STARTING POINT)
    </p>
    <p style="margin-left: 35px; text-indent: -20px; margin-top: 0px"> NEXT SIBLING TAG
        <A load of html which is the raw branch>
    </p>
    '''
    raw_branches_and_twigs = []

    ns = headword_tag.parent

    while True:
        ns = ns.next_sibling
        if isinstance(ns, Tag):
            mini_soup = BeautifulSoup(str(ns), "html.parser")
            #Have we gone too far? 
            too_far = False

            #Too far - check 1
            #look for variant numbers (roots) in our mini_soup
            variantno_soup = mini_soup.find_all(class_="variantno")
            if not variantno_soup is None:
                #We have at least one variantno
                #We are only concerned if we have at least one which
                #is *outside* the tuakana/teina section
                #If we do, then we have gone 'too far'
                for variantno_tag in variantno_soup:
                    variantno_tag_in_tuakana_teina_section = False
                    for tag in variantno_tag.parents:
                        if tag.name == "nobr":
                            variantno_tag_in_tuakana_teina_section = True
                    if not variantno_tag_in_tuakana_teina_section:
                        too_far = True
            
            #Too far - check 2
            if not mini_soup.find(class_="headword") is None:
                #we have found the next headword in our mini_soup
                too_far = True

            #Too far - check 3
            if (mini_soup.p and mini_soup.get_text() == '\n' and
                len(list(mini_soup.descendants)) == 2):
                #we have found a <p></p>   assuming at end of document
                too_far = True           

            if too_far:
                break #exit loop
            else:
                #it's a bona fide raw branch or raw twig
                raw_branches_and_twigs.append(ns)

        else:
            #keep looping, we don't have a Tag
            pass

    return raw_branches_and_twigs

def partition_raw_branch_or_twig(raw_branch_or_twig_tbp):
    '''
    tbp = to be partitioned
    The purpose of the function partition_raw_branch_or_twig is to partition
    the raw_branch_or_twig passed, into 1 or more parts
    There are 2 basic possibilties

    1. There is no tuakana / teina section ('nobr' tag is used to determine this)
    In this case there will be only 1 part (main part), the unaltered 'raw_branch_or_twig_tbp'

    2. There is a tuakana / teina section ('nobr' tag is used to determine this)
    In this case there will be 2 or more parts (usually 2 I think)
    a) main part
    b) 2nd part (probably the tuakana / teina details)
    c) 3rd part (probably the 'see also' details)
    d) e) f) ..... room for more parts if they exist
    '''

    partitioned_raw_branch_or_twig = []
    if raw_branch_or_twig_tbp.nobr:
        # there is a tuakana / teina section
        # find all the 'nobr' parts
        nobr_parts = raw_branch_or_twig_tbp.find_all('nobr')
        for nobr_part in nobr_parts:
            partitioned_raw_branch_or_twig.append(str(nobr_part))
        
        # extinguish the nobr parts from the raw_branch_or_twig passed
        while True:
            try:
                raw_branch_or_twig_tbp.nobr.decompose()
            except AttributeError:
                break
        partitioned_raw_branch_or_twig.insert(0, str(raw_branch_or_twig_tbp)) 
        
        partitioned_raw_branch_or_twig = [BeautifulSoup(x, "html.parser") for x in  partitioned_raw_branch_or_twig]
    else:
        # no tuakana / teina section
        partitioned_raw_branch_or_twig.append(raw_branch_or_twig_tbp)

    return partitioned_raw_branch_or_twig


def get_branch_number(main_part):
    '''
    this function examines the main_part passed
    returns the branch number if a branch
    returns None if it is a twig
    '''

    #do we have a branch or a twig or a problem!
    is_branch = False #initialise
    is_twig = False #initialise 
    branch_or_twig = main_part.find(class_="majsense")  
    if not branch_or_twig is None:
        #we have found at least one branch
        is_branch = True
    else:
        #Not a branch! Is it a twig?
        branch_or_twig = main_part.find(class_="subentry")
        if not branch_or_twig is None:
            #We have found at least one twig
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

def get_tuakana(raw_branch_or_twig):
    '''
    Given either a raw branch or twig
    Return the tuakana
    Expecting there to be 0 or 1.
    If not an error will be thrown

    Also assuming that all tuakana are branches and not twigs ...
    '''
    # check out the number of tuakana
    tuakana_soup = raw_branch_or_twig.find_all(class_ = "seemastersyn")
    if tuakana_soup:
        if len(tuakana_soup) == 1:
            tuakana = tuakana_soup[0].string
            # get the root number and the branch number if there are any
            root_number = 1 # default, will be updated if there is a variantno
            branch_number = 1 # default, will be updated if there is a majsense
            for ns in tuakana_soup[0].next_siblings:
                if isinstance(ns, Tag):
                    ns_soup = BeautifulSoup(str(ns), "html.parser")
                    if ns_soup.select_one(".variantno"): # root number
                        root_number = ns_soup.select_one(".variantno").string.strip()
                        root_number = int(root_number)
                    if ns_soup.select_one(".majsense"): # branch number
                        branch_number = ns_soup.select_one(".majsense").string.strip()
                        branch_number = int(branch_number)
        else:
            # we have found more than one tuakana
            raise NameError(len(tuakana_soup), " tuakana found, we are assuming 0 or 1")

    else:
        # no tuakana found
        return None

    tuakana_id = Word_ID(root_number, tuakana, branch_number, False, 0)
    print("type of return", type(tuakana_id))
    return tuakana_id


if __name__ == '__main__':
    import sys
    import config
    import json
    import ast
    import pū
    import maoriword as mw
    
    try:
        first_argument = sys.argv[1] #uncomment to run
        #first_argument = "are u sure - if so u need to edit the function" #comment to run
    except IndexError:
        #No argument given
        print ("Please supply a Māori letter as the argument")
        sys.exit()

    if first_argument in pū.all_letters:
        word_trees = create_punakupu_trees(first_argument)
        print ('Done - thanks')
    elif first_argument == 'test':
        word_trees = create_punakupu_trees("test")
    else:
        print ("The first argument must be a Māori letter")
        sys.exit()

    if word_trees:
        # WHAT ON EARTH IS THIS?
        # It looks like an effort to turn the word_trees dictionary into a json file
        # Not sure why I wanted to store things as json files, so I could look at them I think
        # rather than pickle. 

        # the main issue being storing namedtuples in json form

        # this is negatively impacting the namedtuples in the values side
        word_trees_for_json = {(str(k)[len(type(k).__name__) + 1 : -1]).replace('=',':'):v \
                               for k,v in word_trees.items()}

        Word_ID = namedtuple('Word_ID', 'root_number trunk branch_number twig twig_number')
        for tree_part in Word_ID._fields:
            tree_part_to_replace = tree_part + ":"
            tree_part_replacement = "'" + tree_part + "'" + ":"
            word_trees_for_json = {k.replace(tree_part_to_replace, tree_part_replacement): v \
                                   for k,v in word_trees_for_json.items()} 

        word_trees_for_json = {"{"+k+"}":v for k,v in word_trees_for_json.items()}
        
        for k, v in word_trees_for_json.items():
            if v:
                word_trees_for_json[k] = v._asdict()


        #to json the word_tree dictionary
        cf = config.ConfigFile()
        json_path = (cf.configfile[cf.computername]['punakupu_path'])
        json_filename = first_argument + ".json"
        full_json_path = json_path + json_filename
        with open(full_json_path, 'w') as f:
            json.dump(word_trees_for_json, f)

        #from json the word_tree dictionary
        with open(full_json_path,'r') as f:
            word_trees_from_json = json.load(f)

