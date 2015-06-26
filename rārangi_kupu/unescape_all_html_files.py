'''The purpose of this piece of code is to
   unescape all the html files in the current directory
'''

import os
import html
all_files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in all_files:
    if f.endswith('html'):
        with open(f, 'r+') as fyle:
            existing_content = fyle.read()
            new_content = html.unescape(existing_content)
            fyle.seek(0)
            fyle.write(new_content)
            fyle.truncate()
