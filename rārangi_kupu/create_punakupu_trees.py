from bs4 import BeautifulSoup, Tag, NavigableString
from collections import namedtuple
import config
import os
import pprint
import process_html_soup

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
            all_raw_branches_and_twigs = process_html_soup.get_raw_branches_and_twigs(soup, headword_tag)

            for counter, raw_branch_or_twig in enumerate(all_raw_branches_and_twigs):
                #identify each branch and twig by setting
                #branch_number, twig, twig_number for each branch and twig on the tree

                raw_branch_or_twig_tbp = raw_branch_or_twig
                partitioned_raw_branch_or_twig = process_html_soup.partition_raw_branch_or_twig(raw_branch_or_twig_tbp)
                
                branch_number = process_html_soup.get_branch_number(partitioned_raw_branch_or_twig[0])

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

                ttt_leaves = {} # tuakana, teina, titiro
                # Tuakana
                all_tuakana = []
                for partition in partitioned_raw_branch_or_twig:
                    tuakana = get_tuakana(partition)
                    if tuakana:
                        all_tuakana.append(tuakana)

                if all_tuakana:
                    ttt_leaves["tuakana"] = all_tuakana[0]
                else:
                    ttt_leaves["tuakana"] = None

                # Teina
                all_teina = []
                for partition in partitioned_raw_branch_or_twig:
                    teina = get_teina(partition)
                    if teina:
                        all_teina.append(teina)

                if all_teina:
                    ttt_leaves["teina"] = all_teina
                else:
                    ttt_leaves["teina"] = None

                if trunk == "tikotiko":
                    print(ttt_leaves["teina"])

                if word_id in word_trees:
                    #major problem the key already exists!
                    #logic problem - revisit drawing board!
                    print ('key', word_id, 'already exists!')
                    if word_id.trunk == 'Pūtahi-nui-o-Rehua':
                        pass #error in HPK
                    else:
                        raise ValueError
                else:
                    word_trees[word_id] = ttt_leaves

                # print(word_id, "durp")

                # print('-------------------------------')

    return word_trees

def get_tuakana(raw_branch_or_twig):
    '''
    Given either a raw branch or twig
    Return the tuakana
    Expecting there to be 0 or 1.
    If not an error will be thrown
    '''
    # check out the number of tuakana
    tuakana_soup = raw_branch_or_twig.find_all(class_ = "seemastersyn")
    if tuakana_soup:
        if len(tuakana_soup) == 1:
            branch_of_tuakana = tuakana_soup[0].string
            # get the root number and the branch number if there are any
            root_number = 1 # default, will be updated if there is a variantno
            branch_number = 1 # default, will be updated if there is a majsense
            twig = False # default, will be updated if the tuakana is a twig
            for ns in tuakana_soup[0].next_siblings:
                if isinstance(ns, Tag):
                    ns_soup = BeautifulSoup(str(ns), "html.parser")
                    if ns_soup.select_one(".variantno"): # root number
                        root_number = ns_soup.select_one(".variantno").string.strip()
                        root_number = int(root_number)
                    if ns_soup.select_one(".majsense"): # branch number
                        branch_number = ns_soup.select_one(".majsense").string.strip()
                        branch_number = int(branch_number)
                    if ns_soup.select_one(".seesubentry"): # this means that the tuakana is a twig
                        twig = ns_soup.select_one(".seesubentry").string.strip()
                        root_number = 0 # we will have to find this out later, the info is not in the html
                        branch_number = 0 # we will have to find this out later, the info is not in the html
        else:
            # we have found more than one tuakana
            raise NameError(len(tuakana_soup), " tuakana found, we are assuming 0 or 1")

    else:
        # no tuakana found
        return None

    tuakana_id = Word_ID(root_number, branch_of_tuakana, branch_number, twig, 0)

    return tuakana_id


def get_teina(raw_branch_or_twig):
    '''
    Given either a raw branch or twig
    Return the teina
    '''

    all_teina = []
    teina_soup = raw_branch_or_twig.select_one(".slavesyns")
    if teina_soup: 
        # get each link within the teina soup with a title = "kupu taurite"
        teina_links = teina_soup.find_all("a", title="kupu taurite")
        for teina_link in teina_links:
            teina_link_parts = teina_link.contents
            if len(teina_link_parts) == 1:
                teina_link_part = teina_link_parts[0]
                # check we have a navigable string
                if not isinstance(teina_link_part, NavigableString):
                    raise NameError("Expecting a NavigableString ", teina_link_part, type(teina_link_part))

                # get rid of any stray spaces just incase
                teina_link_part = teina_link_part.strip()

                # Three possibilities (examples below)
                # 1. ['hāmeme']
                # 2. ['tūtae (tūtae ruru)']
                # 3. ['(korokio tāranga)']

                root_number = 1 # in all cases
                if teina_link_part[0].isalpha() and teina_link_part[-1].isalpha():
                    # 1
                    branch_of_teina = teina_link_part
                    branch_number = 0 # we are not sure, look at the teina for 'kohi' for example, we will fill it out later
                    twig = False
                elif teina_link_part[0].isalpha() and teina_link_part[-1] == ")":
                    # 2
                    branch_of_teina = teina_link_part.split("(")[0].strip() # the first part
                    branch_number = 1 # probably need to set this to 0 as well
                    twig = teina_link_part[teina_link_part.find("(") + 1:teina_link_part.find(")")] # the bit between the brackets
                elif teina_link_part[0] == "(" and teina_link_part[-1] == ")":
                    # 3
                    branch_of_teina = 0 # we are not sure, we will fill it out later
                    branch_number = 0 # we are not sure, we will fill it out later
                    twig = teina_link_part[1:-1] # the bit between the brackets
                else:
                    raise NameError("Unexpected Value - 1 ", teina_link_part)
            elif len(teina_link_parts) == 2:
                # One possibility (example below)
                # ['tītongi', <sup>2</sup>]
                root_number = int(teina_link_parts[1].string)
                branch_of_teina = teina_link_parts[0].strip()
                branch_number = 1 # may have to set this to 0 as well
                twig = False
            elif len(teina_link_parts) == 3:
                # Two possibilities (examples below)
                # 1. ['whakawiri', <sup>2</sup>, ' (2)']
                # 2. ['papa', <sup>2</sup>, ' (papa atua)']
                branch_of_teina = teina_link_parts[0].strip()
                root_number = int(teina_link_parts[1].string)
                
                teina_link_third_part = teina_link_parts[2].strip()[1:-1] # remove the brackets after stripping
                try:
                    branch_number = int(teina_link_third_part)
                except ValueError:
                    branch_number = 0 # we are not sure, we will fill out later
                    twig = teina_link_third_part
                else:
                    twig = False
                
            else:
                print("HELP")

            teina_id = Word_ID(root_number, branch_of_teina, branch_number, twig, 0)
            all_teina.append(teina_id)

    else:
        # no teina found
        return None

    return all_teina


if __name__ == '__main__':
    import sys
    import config
    import json
    import pū
    
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

        # convert namedtuple into string
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
            try:
                v['tuakana'] = v['tuakana']._asdict()
            except AttributeError:
                # No tuakana
                pass

        #to json the word_tree dictionary
        cf = config.ConfigFile()
        json_path = (cf.configfile[cf.computername]['punakupu_path'])
        json_filename = first_argument + ".json"
        full_json_path = json_path + json_filename
        with open(full_json_path, 'w') as f:
            json.dump(word_trees_for_json, f)

        #from json the word_tree dictionary, this acts as 'some sort' of test
        with open(full_json_path,'r') as f:
            word_trees_from_json = json.load(f)


