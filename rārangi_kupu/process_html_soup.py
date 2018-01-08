from bs4 import BeautifulSoup, Tag, NavigableString


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

