'''The purpose of this piece of code is to
   tidy up the html of all html files in the current
   directory

   REPLACE
   </nobr><p style="margin-bottom: 0px">
   WITH    
   </nobr></p><p style="margin-bottom: 0px">

   REPLACE
   }<p style="margin-bottom: 0px">
   WITH
   }</p><p style="margin-bottom: 0px">

   REPLACE
   </a><p style="margin-bottom: 0px">
   WITH
   </a></p><p style="margin-bottom: 0px">

   In all cases we are effectively adding a </p> tag
   This allows the next_sibling functionality to work correctly
   in the create_word_trees functionality
'''

import os
import html
all_files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in all_files:
    if f.endswith('html'):
        with open(f, 'r+') as fyle:
            existing_content = fyle.read()
            new_content = existing_content.replace('</nobr><p style="margin-bottom: 0px">',
                                                   '</nobr></p><p style="margin-bottom: 0px">')

            new_content = new_content.replace('}<p style="margin-bottom: 0px">',
                                              '}</p><p style="margin-bottom: 0px">')

            new_content = new_content.replace('</a><p style="margin-bottom: 0px">',
                                              '</a></p><p style="margin-bottom: 0px">')
            
            fyle.seek(0)
            fyle.write(new_content)
            fyle.truncate()
