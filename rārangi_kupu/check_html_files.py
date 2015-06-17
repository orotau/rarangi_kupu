from create_dict_from_excel import SpreadSheet
import config

def validate(letter):

    """This module contains a function to examine the relationship
       between the Excel spreadsheet and the html files created from it

       Namely

       a) Does every unique headword in the spreadsheet have a corresponding
          html file? If not, which are missing?

       b) Are their more html files than there should be? If so, what are they?
    """


    words_dict = SpreadSheet(letter).pulldata()
    headword_variant = list(words_dict.keys())

    # get the dump path
    cf = config.ConfigFile()
    dump_folder = (cf.configfile[cf.computername]['dump_path'])


    target_folder = dump_folder + letter + "/"


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
