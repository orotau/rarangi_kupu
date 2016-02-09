'''
This module contains the regexes used in
the word frequency work
'''

# Get the non-compound maori words using regex
maori_word = r"""
\b                      # capture whole words only

(?:

(?:                     # group so we can use the +
                        # non-capturing so the whole word is returned
ng|                     # needs to be before the n
wh|                     # needs to be before the w and h
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

capitalised_word = r"""

(?:
                 
(?:
\b
[AEIOUĀĒĪŌŪHKMNPRTW]    #capital letter to start
\w+                     #one or more alphanumeric characters
\b
)

)
"""
