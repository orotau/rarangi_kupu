from bs4 import BeautifulSoup, Tag
from create_dict_from_excel import SpreadSheet
import config

def validate(letter):

    '''This code checks the quality of the words typed into the Excel Spreadsheet
       by examining the web pages pulled from I-Papakupu
       that were found using the words typed into the spreadsheet

       It will pick up the following 2 errors

       1) Word in spreadsheet not found in I-Papakupu (misspelt probably)
       2) Word / Variant combo in spreadsheet not found in I-Papakupu
    '''


    words_dict = SpreadSheet(letter).pulldata()
    headword_variant = list(words_dict.keys())

    # get the dump path
    cf = config.ConfigFile()
    dump_folder = (cf.configfile[cf.computername]['dump_path'])


    target_folder = dump_folder + letter + "/"

    for k in headword_variant:
        target_filename = k[0] + ".html"
        target_file = target_folder + target_filename

        try:
            with open(target_file, 'rb') as f:
                soup = BeautifulSoup(f.read())
        except FileNotFoundError:
            try:
                with open(target_file[:-1], 'rb') as f:  # htm
                    soup = BeautifulSoup(f.read())
            except FileNotFoundError:
                print('***No file found for***', k[0])
            except:
                raise
        except:
            raise

        headwords = soup.find_all(class_="headword")

        if headwords:
            # pair up the headword(s) on the page with their variants
            # if there is no varaiant for a headword then the variant
            # will be set to ''
            keys_on_page = []
            for hw in headwords:
                VariantFound = False
                ns = hw
                while True:
                    ns = ns.next_sibling
                    if isinstance(ns, Tag):
                        keys_on_page.append((hw.string, int(ns.string)))
                        VariantFound = True
                    else:
                        pass

                    if ns is None:
                        # check to see if we found a variant or not
                        if not VariantFound:
                            # we haven't found a variant
                            keys_on_page.append((hw.string, ''))
                        break

        # print out the relevant information (separated for readability)

        if headwords:
            #print(keys_on_page)
            if k in keys_on_page:
                pass
            else:
                #found a match of sorts but not exact match
                #CaSe or macrons or variant will be the issue
                print("Check CaSe / Macrons / Variant Number", k)
        else:
            #misspelling (probably)
            print("no headword found for", k , "misspelling (probably)")

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
