from bs4 import BeautifulSoup, Tag
from collections import namedtuple
import config
import os
import pprint

def create_word_trees(letter):
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

    #create named tuple to store unique keys
    Word_ID = namedtuple('Word_ID', 'root_number trunk branch_number twig twig_number')

    # get the dump path
    cf = config.ConfigFile()
    dump_folder = (cf.configfile[cf.computername]['dump_path'])
    target_folder = dump_folder + letter + "/"

    #get all the files in the target folder (exclude backup files, ending with tilde)
    html_file_names = [f for f in os.listdir(target_folder) if not f.endswith('~')]

    #open the html files for the letter
    for fyle in html_file_names:
        with open(target_folder + fyle) as f: #read only
            soup = BeautifulSoup(f.read())

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

                branch_number = get_branch_number(raw_branch_or_twig)

                if not branch_number is None:
                    #we have a branch
                    branch_number_set = True
                    branch_number_for_twig = branch_number
                    twig = False #twig always False for a branch
                    twig_number = 0 #twig_number always 0 for a branch (*)
                else:
                    #we have a twig
                    twig = raw_branch_or_twig.find(class_="subentry").string

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
                print(word_id)

                leaves = {} #  9 keys in all
                atua = get_atua(raw_branch_or_twig) #1
                leaves["atua"] = atua

                reo_kē = is_reo_kē(raw_branch_or_twig) #2
                leaves["reo_kē"] = reo_kē

                hou = is_hou(raw_branch_or_twig) #3
                leaves["hou"] = hou

                whakamāoritanga = get_whakamāoritanga(raw_branch_or_twig) #4
                leaves["whakamāoritanga"] = whakamāoritanga

                tauira = get_tauira(raw_branch_or_twig) #5
                leaves["tauira"] = tauira

                whakamahinga_kupu_1 = get_primarywordclass(raw_branch_or_twig) #6
                leaves["whakamahinga_kupu_1"] = whakamahinga_kupu_1

                whakamahinga_kupu_2 = get_secondarywordclasses(raw_branch_or_twig) #7
                leaves["whakamahinga_kupu_2"] = whakamahinga_kupu_2

                pīmuri_whakahāngū = get_passives(raw_branch_or_twig) #8
                leaves["pīmuri_whakahāngū"] = pīmuri_whakahāngū

                pīmuri_whakaingoa = get_nominalisations(raw_branch_or_twig) #9
                leaves["pīmuri_whakaingoa"] = pīmuri_whakaingoa

                if word_id in word_trees:
                    #major problem the key already exists!
                    #logic problem - revisit drawing board!
                    print ('key', word_id, 'already exists!')
                    if word_id.trunk == 'Pūtahi-nui-o-Rehua':
                        pass #error in HPK
                    else:
                        raise ValueError
                else:                
                    word_trees[word_id] = leaves

                #print(word_id, "durp")
                #pprint.pprint(leaves)
                #print('-------------------------------')

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
            mini_soup = BeautifulSoup(str(ns))
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


def get_branch_number(raw_branch_or_twig):
    '''
    this function examines the raw_branch_or_twig passed
    returns the branch number if a branch
    returns None if it is a twig
    '''

    #remove the tuakana/teina section if it exists
    #The nobr tag is used to deliniate this
    try:
        raw_branch_or_twig.nobr.decompose()
    except AttributeError:
        #there is no tuakana/teina section
        pass

    #do we have a branch or a twig or a problem!
    is_branch = False #initialise
    is_twig = False #initialise 
    branch_or_twig = raw_branch_or_twig.find(class_="majsense")  
    if not branch_or_twig is None:
        #we have found at least one branch
        is_branch = True
    else:
        #Not a branch! Is it a twig?
        branch_or_twig = raw_branch_or_twig.find(class_="subentry")
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

def get_atua(raw_branch_or_twig):
    '''
    Given either a raw branch or twig
    Return a list of the atua
    Expecting there to be atua.
    If not some error will be thrown
    '''
    atua_soup = raw_branch_or_twig.find(class_="atua")
    atua = atua_soup.string.split(',')
    atua = [x.strip() for x in atua]
    return atua

def is_reo_kē(raw_branch_or_twig):
    '''
    Given either a raw branch or twig
    Return True (reo kē) or False
    '''
    usage_soup = raw_branch_or_twig.find(class_="usage")
    if usage_soup:
        if 'reo kē' in usage_soup.string:
            return True
        else:
            return False
    else:
        return False

def is_hou(raw_branch_or_twig):
    '''
    Given either a raw branch or twig
    Return True (hou) or False
    '''
    usage_soup = raw_branch_or_twig.find(class_="usage")
    if usage_soup:
        if 'hou' in usage_soup.string:
            return True
        else:
            return False
    else:
        return False

def get_whakamāoritanga(raw_branch_or_twig):
    '''
    Given either a raw branch or twig
    Return the whakamāortianga if it exists
    Return '' and print message otherwise
    '''

    whakamāoritanga_soup = raw_branch_or_twig.find(class_="definition")
    try:
        return whakamāoritanga_soup.string
    except AttributeError:
        #there is no definition (p.36 arumoni for example)
        print ('no defintion in soup' , raw_branch_or_twig)
        return ''

def get_tauira(raw_branch_or_twig):
    '''
    Given either a raw branch or twig
    Return the tauira
    Expecting there to be at least one.
    If not some error will be thrown (NoneType object is not iterable)

    There is the possibility that within the example there is another tag 
    examplehighlight, which means a little more complexity.
    '''
    tauira = []
    tauira_soup = raw_branch_or_twig.find_all(class_="example")
    for tauira_mini_soup in tauira_soup:
        tauira_mini_soup_string = tauira_mini_soup.string
        if not tauira_mini_soup_string:
            #cannot find tauira text due to assumed presence of examplehighlight tag
            tauira_parts = list(tauira_mini_soup.strings)
            tauira_mini_soup_string = ''.join(tauira_parts)
        tauira.append(tauira_mini_soup_string)
    return tauira

def get_primarywordclass(raw_branch_or_twig):
    '''
    Given either a raw branch or twig
    Return the primary word class
    It is possible that there may be no primary word class 
    (Don't really know why but it certainly happens in the dictionary)
    I don't know if there can be more than one
    but a return value of None will possibly point to this.
    '''
    primarywordclass_soup = raw_branch_or_twig.find(class_="primarywordclass")
    if primarywordclass_soup:
        return primarywordclass_soup.string
    else:
        return ""

def get_secondarywordclasses(raw_branch_or_twig):
    '''
    Given either a raw branch or twig
    Return the secondary word class(es)
    It is possible that there may be no secondary word class 
    There can be more than one.
    '''
    secondary_word_classes = []
    secondarywordclass_soup = raw_branch_or_twig.find(class_="secondarywordclass")
    if secondarywordclass_soup:
        secondary_word_classes = list(secondarywordclass_soup.strings) 
        # remove ', ' list entries     
        secondary_word_classes = [x for x in secondary_word_classes if x != ", "]
    return secondary_word_classes

def get_passives(raw_branch_or_twig):
    '''
    Given either a raw branch or twig
    Return the 'passives' as a list
    There may be 0, 1 or more
    We will assume entries distinguished with a space
    '''
    passives = []
    passives_soup = raw_branch_or_twig.find(class_='passivised')
    if passives_soup:
        passives = passives_soup.string.split(" ")
    return passives

def get_nominalisations(raw_branch_or_twig):
    '''
    Given either a raw branch or twig
    Return the 'nominalisations' as a list
    There may be 0, 1 or more
    We will assume entries distinguished with a space
    '''
    nominalisations = []
    nominalisations_soup = raw_branch_or_twig.find(class_='nominalised')
    if nominalisations_soup:
        nominalisations = nominalisations_soup.string.split(" ")
    return nominalisations        

if __name__ == '__main__':
    import sys
    import config
    import json
    import ast
    import pū
    import maoriword as mw
    
    try:
        #first_argument = sys.argv[1] #uncomment to run
        first_argument = "are u sure - if so u need to edit the function" #remove to run
    except IndexError:
        #No argument given
        print ("Please supply a Māori letter as the argument")
        sys.exit()

    if first_argument in pū.all_letters:
        word_trees = create_word_trees(first_argument)
        print ('Done - thanks')
    elif first_argument == 'test':
        word_trees = create_word_trees("test")
    else:
        print ("The first argument must be a Māori letter")
        sys.exit()

    if word_trees:

        word_trees_for_json = {(str(k)[len(type(k).__name__) + 1 : -1]).replace('=',':'):v \
                               for k,v in word_trees.items()}

        Word_ID = namedtuple('Word_ID', 'root_number trunk branch_number twig twig_number')
        for tree_part in Word_ID._fields:
            tree_part_to_replace = tree_part + ":"
            tree_part_replacement = "'" + tree_part + "'" + ":"
            word_trees_for_json = {k.replace(tree_part_to_replace, tree_part_replacement): v \
                                   for k,v in word_trees_for_json.items()} 

        word_trees_for_json = {"{"+k+"}":v for k,v in word_trees_for_json.items()}

        #to json the word_tree dictionary
        cf = config.ConfigFile()
        json_path = (cf.configfile[cf.computername]['json_path'])
        json_filename = first_argument + ".json"
        full_json_path = json_path + json_filename
        with open(full_json_path, 'w') as f:
            json.dump(word_trees_for_json, f)

        #from json the word_tree dictionary
        with open(full_json_path,'r') as f:
            word_trees_from_json = json.load(f)

