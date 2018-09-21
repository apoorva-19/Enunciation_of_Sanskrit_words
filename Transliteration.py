#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 22:01:41 2018

@author: apoorva
"""
# to run you first need to install cltk
# pip install cltk

from cltk.corpus.sanskrit.itrans.unicode_transliterate import ItransTransliterator
from cltk.tokenize.sentence import TokenizeSentence
from cltk.stem.sanskrit.indian_syllabifier import Syllabifier

lang = 'hi'
language = 'hindi'
tokenizer = TokenizeSentence('sanskrit')
syl = Syllabifier(language)

if __name__ == '__main__':
    import sys

if len(sys.argv) == 1:
    print('Needs filename for splitting shlokas')
    sys.exit(-1)
elif len(sys.argv) == 2:
    print('Needs filename for storing split shlokas')
    sys.exit(-1)

# to avoid numbers and punctuation marks


def check_token(token):
    flag = True
    if token == '।':
        flag = False
    elif token.isdigit():
        flag = False

    return flag


infilename = sys.argv[1]
outfilename = sys.argv[2]
filestring = []

infile = open(infilename, "r")

string = infile.readline()
while string:
    string = string[:-1]
    filestring.append(string)
    string = infile.readline()

infile.close()
outfile = open(outfilename, "w")

# shlok = u'एवं सततयुक्ता ये भक्तास्त्वां पर्युपासते। येचाप्यक्षरमव्यक्तं तेषां के योगवित्तमाः।।12.1।।'
for shlok in filestring:
        # picking one shloka from the file
    t_shlok = tokenizer.tokenize(shlok)
    # initializing the flags
    count = 0  # to count the number of phonemes after which the split has to be done
    pos = 0  # to insert the -
    diff = 0  # to keep track of the overflow phonemes
    for i in range(len(t_shlok)):
        token = t_shlok[i]
        split = syl.orthographic_syllabify(token)
        l = len(split)
        #phonemes already covered
        prev = count
        #checking for purna-viram and numbers
        if l == 1 and check_token(token) == False:
            diff = pos = count = 0
            continue
        #more phonemes added
        count = count + l
        if count > 8:
            #checks for the presence of rafar on the last phoneme
            trans_token = ItransTransliterator.to_itrans(split[8 - prev - 1], lang)
            if trans_token.startswith('r') and len(trans_token) > 1:
                #shifting the last phoneme to the next word
                diff = l - 8 + prev + 1
                #position for splitting the word
                pos = 8 - prev + 1
            else:
                #rafar not present
                diff = l - 8 + prev
                #position to split the word
                pos = 8 - prev
                #set the count to 0
                count = 0
        elif count == 8:
            count = 0
        while diff > 0:
            #splitting the word
            if pos != l - 1:
                split.insert(pos, '-')
            #joining a word
            token = ''.join(map(str, split))
            # split it again to break the word again
            split = syl.orthographic_syllabify(token)
            if diff <= 8:
                count = diff
                pos = diff = 0
                t_shlok[i] = ''.join(map(str, split))
            else:
                diff = diff - 8
                pos = pos + 8

        # joining the words together to form the shloka
    broken = ' '.join(map(str, t_shlok))
    outfile.write(broken + "\n")

outfile.close()

# trans_shlok = {ItransTransliterator.to_itrans(word,lang) for word in t_shlok}

# for t_word in trans_shlok:
#    print(t_word)
