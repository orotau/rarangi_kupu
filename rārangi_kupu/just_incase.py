just in case

#print those tauira that don't contain their 'headword'
'''
for k,v in all_entries_with_tauira.items():
    if not k.twig:
        key_word = k.trunk
    else:
        key_word = k.twig

    for t in v["tauira"]:
        if key_word.lower() not in t.lower():
            if key_word.startswith('-') or key_word.endswith('-'):
                #not interested in prefixes or suffixes
                pass
            else:
                print (key_word, "SPACE", t)

return False
''' 
