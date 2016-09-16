import pprint
import pataka
import words_and_frequencies
import config

HPK_ALL_FILE_NAME = "hpk_all.txt"
# all the word in HPK, Entries, SubEntries, Passives and Nominalisations

cf = config.ConfigFile()
hpk_all_path = (cf.configfile[cf.computername]
                                          ['text_files_path'])

hpk_all = []
letters_and_count = {}
letter_frequency = []

hpk_all_file_path = \
hpk_all_path + HPK_ALL_FILE_NAME

with open(hpk_all_file_path, 'r') as f:
    for line in f:
        hpk_all.append(line.replace('\n', ''))

print(len(hpk_all))

waf = words_and_frequencies.waf
all_words = [x[0] for x in waf]

extras = list(set(all_words) - set(hpk_all))

squash = [(x, y) for (x, y) in waf if x in extras]

kount = 0
for x in squash:
    if x[0] == x[0].lower():
        kount = kount + 1
        print (kount, x[0], ",", x[1])

print (len(squash))



