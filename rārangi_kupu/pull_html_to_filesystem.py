'''The purpose of this piece of code is to

   pull HTML pages from the HPK web site so that

       1)I don't need to keep hitting it
       2)What is done subsequently will be quicker

   The number of keys in the python dictionary will NOT
   translate into the number of files on the file system
   because

       a)A file will *not* be created for any variants
         So 'a' which has 4 variants will only produce 1 HTML file

       b)This applies to Windows only
         If 2 headwords only differ by case (e.g. 'Āpotoro' and 'āpotoro')
         only 1 HTML file will be created (note it could be either
         'Āpotoro.html' or 'āpotoro.html') depending on the order of the
         entries in the python dictionary.

   Also need a testing suite
'''
import os.path
import urllib.request
from urllib.parse import quote
from urllib.error import URLError
from create_dict_from_excel import SpreadSheet
import config


class HTMLPageGrabber():

    def __init__(self, letter):
        '''get the list of headwords to be used to do searches
        '''
        self.letter = letter

        words_dict = SpreadSheet(self.letter).pulldata()
        self.headword_list = [x[0] for x in words_dict.keys()]

        # get the 3 parts of the URL
        cf = config.ConfigFile()
        self.url1of3 = (cf.configfile[cf.computername]['url1OF3'])
        self.url2of3 = (cf.configfile[cf.computername]['url2OF3'])
        self.url3of3 = (cf.configfile[cf.computername]['url3OF3'])

        # get the user agent name (we need this otherwise
        # the macrons get stripped off when query is returned)
        self.ua = (cf.configfile[cf.computername]['ua'])

        # get the dump folder
        self.dump_folder = (cf.configfile[cf.computername]['dump_path'])

    def pullwebpages(self):

        target_folder = (self.dump_folder + self.letter + "/")
        
        for hw in self.headword_list:

            target_filename = hw + ".html"
            target_file = target_folder + target_filename

            if not os.path.isfile(target_file):                
                url = self.url1of3 + self.url2of3 + quote(hw) + self.url3of3
                print(hw)
                ua = self.ua
                headers = {'User-Agent': ua}
                request = urllib.request.Request(url, None, headers)

                try:
                    response = urllib.request.urlopen(request)
                except URLError as e:
                    if hasattr(e, 'reason'):
                        print('We failed to reach a server.')
                        print('Reason: ', e.reason)
                    elif hasattr(e, 'code'):
                        print('The server couldn\'t fulfill the request.')
                        print('Error code: ', e.code)
                else:
                    print(target_file)
                    with open(target_file, 'xb') as f:
                        f.write(response.read())

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
        #initialise the HTML page grabber
        html_page_grabber = HTMLPageGrabber(first_argument)
        html_page_grabber.pullwebpages()
        print ('Done - thanks')
    else:
        print ("The first argument must be a Māori letter")
        sys.exit()
