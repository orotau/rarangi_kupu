'''
This module contains the regexes used in
the word frequency work
'''

maori_word = r"""
\b                      # capture whole words only

(?:

(?:                     
ng                      # needs to be before the n
|
wh                      # needs to be before the w and h
|
[hkmnprtw]
)
?                       # 0 or 1 times

(?:
[aeiouāēīōū]
)

)                      
+                       # one or more of the above
\b
"""

sequential_capitalised_words = r"""

(?:
[A-ZĀĒĪŌŪ]              # capital letter to start
[a-zāēīōū]+             # one or more alphanumeric characters
\s+                     # one or more spaces
)
+                       # one or more

(?:
\b
[A-ZĀĒĪŌŪ]              # capital letter to start
[a-zāēīōū]+             # one or more alphanumeric characters
\b
)

(?!
-                       # Don't bump into a closed compound
)

"""

closed_compound = r"""

(?:    

(?:
\w+                     # one word 
)

(?:  
-                       # dash
\w+                     # one word
)+                      # one or more times

)
"""

capitalised_non_closed_compound_word = r"""

(?<!
-                       # Don't select part of a closed compound
)
               
(?:
\b
[A-ZĀĒĪŌŪ]              # capital letter to start
[a-zāēīōū]*             # zero or more alphabetic characters
\b
)

(?!
-                       # Don't select part of a closed compound
)
"""


sentence_boundaries = r"""

(?:
\A                      # Start of text chunk only
['"]                    # single or double quote
[ ]*                    # 0, 1 or more spaces
)

|                       # or

(?:
[ ]+                    # 1 or more spaces
['"]                    # single or double quote
[ ]*                    # 0, 1 or more spaces
)

|

(?:
[?!]
[ ]+
)

|

(?:
(?<!            #Avoid matching a name like T. D. Smith
[ ]             #works so long as it is not the first thing in the text chunk
[A-Z]
)
[.]
[ ]+
)

"""
