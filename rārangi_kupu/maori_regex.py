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
[ ]+                     # one or more spaces
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

isolated_closed_compound_word = r"""

(?:    

(?:
[A-Za-zĀĒĪŌŪāēīōū]+     # one word 
)

(?:  
-                       # dash
[A-Za-zĀĒĪŌŪāēīōū]+     # one word
)+                      # one or more times

)
"""

mixed_open_compound = r"""

# capitalised non-closed-compound word
(?:
\b
[A-ZĀĒĪŌŪ]              # capital letter to start
[a-zāēīōū]*             # zero or more alphabetic characters
[ ]+                    # 1 or more spaces
)


# capitalised closed compound
(?:    

(?:
[A-ZĀĒĪŌŪ]              # capital letter to start
[a-zāēīōū]+              
)

(?:  
-                       # dash
[A-Za-zĀĒĪŌŪāēīōū]+     # one word
)+                      # one or more times

)
"""

capitalised_non_compound_word = r"""

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

lower_case_non_compound_word = r"""

(?<!
-                       # Don't select part of a closed compound
)
               
(?:
\b
[a-zāēīōū]+             # one or more alphabetic characters
\b
)

(?!
-                       # Don't select part of a closed compound
)
"""

sentence_boundaries = []


sentence_boundaries.append(r"""


(?:
\A                      # Start of text chunk only
['"]                    # single or double quote
[ ]*                    # 0, 1 or more spaces
)

""")

sentence_boundaries.append(r"""

(?:
[ ]+                    # 1 or more spaces
['"]                    # single or double quote
[ ]*                    # 0, 1 or more spaces
)

""")

sentence_boundaries.append(r"""

(?:
[:]
[ ]+
)

""")

sentence_boundaries.append(r"""

(?:
[.?!]
['"]?
[ ]+
)

""")

sentence_boundaries.append(r"""
(?:
(?<!            #Avoid matching a name like T. D. Smith
[ ]             #works so long as it is not the first thing in the text chunk
[A-Z]
)
[.]
[ ]+
)

""")

misc = r"""
(?:
[^A-Za-zĀĒĪŌŪāēīōū\W]+
)
"""

