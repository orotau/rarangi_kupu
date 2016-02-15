'''
This module contains the regexes used in
the word frequency work
'''

##################################################################
#1 Open Compounds - "oc"
##################################################################
def get_oc_regex(open_compound):
    '''
    This function gets the open compound to search for
    and returns the regex that will find it
    Ensures that we don't consume part of a closed compound
    '''

    oc_regex_start = r"""
    (?<!
    -                   # Don't select part of a closed compound
    )
    """

    oc_regex_middle = r"\b" + open_compound + r"\b"

    oc_regex_end = r"""
    (?!
-                       # Don't select part of a closed compound
    )
    """

    return oc_regex_start + oc_regex_middle + oc_regex_end

    
static_regexes = []
##################################################################
#Group 2 - Vanilla Open Compounds
##################################################################
static_regexes.insert(0, ("voc", r"""
(?:
[A-ZĀĒĪŌŪ]              # capital letter to start
[a-zāēīōū]+             # one or more alphanumeric characters
[ ]+                    # one or more spaces
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
))

##################################################################
#Group 3 - Mixed Open Compounds
##################################################################
static_regexes.insert(1, ("moc", r"""
# first - capitalised non-closed-compound word
(?:
\b
[A-ZĀĒĪŌŪ]              # capital letter to start
[a-zāēīōū]*             # zero or more alphabetic characters
[ ]+                    # 1 or more spaces
)


# second - capitalised closed compound
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
))

##################################################################
#Group 4 - Isolated Capitalised Non-Compound Word
# The regex will find all Capitalised Non-Compound Words
# but if they are contained in Compound Words previously found
# they will be rejected (classed as "all inside")
# resulting in isolated.
##################################################################
static_regexes.insert(2, ("icncw", r"""

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
))

##################################################################
#Group 5 - Isolated Closed-Compound Words
# The regex will find all Closed-Compound Words
# but if they are contained in Mixed Open Compound Words previously found
# they will be rejected (classed as "all inside")
# resulting in isolated.
##################################################################
static_regexes.insert(3, ("iccw", r"""

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
))

##################################################################
# Group 6 - Isolated Lower Case Non-Compound Word
# The regex will find all Lower Case Non-Compound Words
# but if they are contained in Compound Words previously found
# they will be rejected (classed as "all inside")
# resulting in isolated.
##################################################################
static_regexes.insert(4, ("ilcncw", r"""
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
))

##################################################################
# Group 7 - Punctuation and Whitespace
##################################################################
static_regexes.insert(5, ("paws", r"""
(?:
\W+
)
"""
))

##################################################################
# Group 8 - Everything Else
##################################################################
static_regexes.insert(6, ("misc", r"""
(?:
[^A-Za-zĀĒĪŌŪāēīōū\W]+
)
"""
))


sentence_boundaries = []

sentence_boundaries.insert(0, r"""


(?:
\A                      # Start of text chunk only
['"]                    # single or double quote
[ ]*                    # 0, 1 or more spaces
)

""")

sentence_boundaries.insert(1, r"""

(?:
[ ]+                    # 1 or more spaces
['"]                    # single or double quote
[ ]*                    # 0, 1 or more spaces
)

""")

sentence_boundaries.insert(2, r"""

(?:
[:]
[ ]+
)

""")

sentence_boundaries.insert(3, r"""

(?:
[.?!]
['"]?
[ ]+
)

""")

sentence_boundaries.insert(4, r"""
(?:
(?<!            #Avoid matching a name like T. D. Smith
[ ]             #works so long as it is not the first thing in the text chunk
[A-Z]
)
[.]
[ ]+
)

""")



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

