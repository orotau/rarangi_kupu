"""
The Māori letter groups to be used in the project
"""

digraphs = ('wh','ng','WH','NG','Wh','Ng','wH','nG')

vowels = ('a', 'e', 'i', 'o', 'u',
          'A', 'E', 'I', 'O', 'U')

macronised_vowels = ('ā', 'ē', 'ī', 'ō', 'ū',
                     'Ā', 'Ē', 'Ī', 'Ō', 'Ū')

consonants = ('h', 'k', 'm', 'n', 'p', 'r', 't', 'w',
              'H', 'K', 'M', 'N', 'P', 'R', 'T', 'W')

#dictionary_letters = ('A', 'E', 'H', 'I', 'K', 'M', 'N', 'Ng', 'O', 'P', 'R', 'T', 'U', 'W', 'Wh')
dictionary_letters = ('T',)
all_letters = digraphs + vowels + macronised_vowels + consonants

intra_word_punctuation = [' ', '-']
inter_word_punctuation = ', '
