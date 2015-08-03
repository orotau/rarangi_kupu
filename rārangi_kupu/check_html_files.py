import config
import os
from create_dict_from_excel import SpreadSheet

def validate(letter):

    """This module contains a function to examine the relationship
       between the Excel spreadsheet and the html files created from it

       Namely

       a) Does every unique headword in the spreadsheet have a corresponding
          html file?

       b) Are their more html files than there should be? If so, what are they?
    """

    #get all the unique headwords in the spreadsheet
    words_dict = SpreadSheet(letter).pulldata()
    unique_headwords = set([x[0] for x in list(words_dict.keys())])

    # get the dump path
    cf = config.ConfigFile()
    dump_folder = (cf.configfile[cf.computername]['dump_path'])
    target_folder = dump_folder + letter + "/"

    #get all the files in the target folder
    html_file_names = os.listdir(target_folder)
    html_file_names_no_extension = set([x.split('.html')[0] for x in html_file_names])

    #Does every unique headword have a corresponding html file?
    if unique_headwords.issubset(html_file_names_no_extension):
        print ("Every unique headword has an html file")
    else:
        print ("html files missing - run pull_html_to_filesystem.py")

    #Do we have too many html files?
    if html_file_names_no_extension > unique_headwords:
        print ("Too many html files - get rid of this / these...")
        print (html_file_names_no_extension.difference(unique_headwords))
        
    return
    

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
        validate(first_argument)
        print ('Done - thanks')
    else:
        print ("The first argument must be a Māori letter")
        sys.exit()
