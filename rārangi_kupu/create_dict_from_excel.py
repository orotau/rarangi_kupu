'''This is the Python starting point for the rārangi kupu project

   The purpose of this piece of code is 

   1. Pull Headword / Variant information from an Excel Spreadsheet
      into a Python Dictionary in the format
      {(Headword, Variant): (Page Number, Number on Page, Overall Number)}

   2. Check that we have no 'Headword / Variant' duplicates

      We are *not* checking the words in the spreadsheet match 
      the words they have been copied from. That happens elsewhere.
'''
import config
from xlrd import open_workbook

class SpreadSheet():

    def __init__(self, letter):
        '''open the spreadsheet for the letter
        '''
        cf = config.ConfigFile()
        wb_path = (cf.configfile[cf.computername]['excel_folder'] +
                   cf.configfile['default'][letter + '_excel_filename'])
        # print(wb_path) debug
        self.wb = open_workbook(wb_path)

    def pulldata(self):
        '''pull the data from the spreadsheet into a python dictionary
           In xlrd - column first, then row
           first column is column 0, first row is row 0

           If a dictionary page hols no data (e.g. p 433) no information is added
           to the dictionary. This was accident rather than by design but doesn't
           seem to cause any issues.
        '''
        return_dict = {}

        for s in self.wb.sheets():

            headwords = s.col_values(0, 1)  # column 1, row 2
            variants = s.col_values(1, 1)   # column 2, row 2

            assert len(headwords) == len(variants), \
                "Unexpectedly Headwords and Variants don't match"

            #'' if there is no variant, the variant number otherwise
            for n, val in enumerate(variants):
                try:
                    variants[n] = int(val)
                except ValueError:
                    variants[n] = ""

            # page keys
            pagekeys = list(zip(headwords, variants))

            # check that the pagekeys are unique
            if len(pagekeys) == len(set(pagekeys)):
                # sweet they are unique
                pass
            else:
                print("Duplicate Headword/Variant pair on page", s.name)
                exit()

            # page data
            pagedata = (list(zip(
                [int(s.name)]*len(pagekeys),  # Page Number
                range(1, len(pagekeys)+1),  # Number on Page
                range(len(return_dict) + 1,
                      len(pagekeys) + len(return_dict) + 1))))  # Overall Numbr

            # get the dictionary entries for the page
            pagedict = dict(list(zip(pagekeys, pagedata)))

            # check that the headword/variant pair does not already exist
            for k in pagedict.keys():
                if k in return_dict.keys():
                    print("Found already existing Headword/Variant pair on page",
                          s.name, k)
                    exit()
                else:
                    pass

            # add the keys and data for the page to the dictionary for the letter
            return_dict.update(pagedict)

            # print the page and the number on each page
            #print ("Page", s.name, "Entries", len(pagedict))

        return return_dict


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
        words_dict = SpreadSheet(first_argument).pulldata()

        #A reminder this is what each dictionary entry looks like
        #{(Headword, Variant): (Page Number, Number on Page, Overall Number)}

        #Key  (Headword, Variant)
        #Value  (Page Number, Number on Page, Overall Number)

        #Display for each page
        #Letter, Page Number, Raw Count of Headwords
        #e.g.
        #A Page 1 Raw Count 11
        #A Page 2 Raw Count 13
        #A Page 3 Raw Count 13
        #A Page 4 Raw Count 14 ...

        from collections import Counter
        all_page_numbers = [x[0] for x in list(words_dict.values())]
        for page, raw_count in Counter(all_page_numbers).items():
            print (first_argument, 'Page', page, 'Raw Count', raw_count)

        #Sum the total
        print (first_argument, 'Total Raw Count', len(words_dict))

        #Get the total number of unique headwords (ignoring Variants)
        #This should correspond to the number of HTML files generated
        unique_headwords = set([x[0] for x in list(words_dict.keys())])
        print (first_argument, 'Total Unique Headwords (html files)', len(unique_headwords))

    else:
        print ("The first argument must be a Māori letter")
        sys.exit()



