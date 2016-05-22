def tki_files():

    import csv
    from collections import Counter

    tki_ordered_file = []

    with open('tki_word_freq_ordered.csv') as tki_ordered:
        tki_ordered = csv.reader(tki_ordered)
        for word in tki_ordered:
            tki_ordered_file.append(word[0].strip())

    

if __name__ == '__main__':
    tki_files()
