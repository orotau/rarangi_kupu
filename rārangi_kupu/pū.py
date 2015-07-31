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

legal_punctuation = (' ', '-')

all_letters = digraphs + vowels + macronised_vowels + consonants

all_legal_characters = all_letters + legal_punctuation
