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
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate

lang = 'hi'
language = 'hindi'
tokenizer = TokenizeSentence('sanskrit')
syl = Syllabifier(language)
check_phonemes_1 = ['ः', 'ऽ']
check_phonemes_2 = ['ङ्‍', '\u200c']

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

#due to the presence of : and other conjuct consonants as well as special matras, the word is sometimes split 
#incorrectly hence to avoid that the followig function checks the proximity of the splitting position to the 
#purna_viram. If there is a single phoneme which might be considered as one or two phonemes depending on 
#transliteration done by ITRANS

def check_proximity(split, pos, next_token):
    if len(split) - pos in range(1,3):
        if next_token == '।' or next_token == '॥' or ItransTransliterator.to_itrans(next_token, lang).isdigit:
            return False

    return True

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
        if '\u200c' in split:
            l -= 2
        #phonemes already covered
        prev = count
        #checking for purna-viram and numbers
        if l == 1 and check_token(token) == False:
            diff = pos = count = 0
            continue
        #more phonemes added
        count = count + l
        print(count)
        print(l)
        print(split)
        #word extends the meter length
        if count > 8:
            #rafar not present
            diff = l - 8 + prev
            #position to split the word
            pos = 8 - prev
            #set the count to 0
            count = 0
            #checks for the presence of rafar on the last phoneme. Here the phoneme should be split in such a way that
            # र् with a halant should be connected to the previous word and the phoneme without the rafar to the
            #next word
            #converting the string to roman script from devanagri script
            trans_token = ItransTransliterator.to_itrans(split[pos], lang)
            if trans_token.startswith('r') and trans_token.startswith('ra') != True:
                #add the character to the phoneme
                split[pos-1] = split[pos-1] + 'र्'
                #extracting the character from the second phoneme
                replace_phoneme = trans_token.replace("r", "")
                #converting the string from roman script to devnagari script
                split[pos] = transliterate(replace_phoneme, sanscript.ITRANS, sanscript.DEVANAGARI)
        #word equal to meter length
        elif count == 8:
            count = 0

        while diff > 0:
            #splitting the word
            if token.find('ऽ') <= pos and token.find('ऽ') > -1:
                    pos += token.count('ऽ')
            #This rule is incorrect. Come to this and fix this later if it creates problems in other cases.
            # if token.find('ऽ') > pos and l-token.find('ऽ') < 3:
            #     pos += token.count('ऽ')
            if token.find('ः') <=pos and token.find('ः') > -1:
                pos +=token.count('ः')
            #the find function is unable to find the character 'ङ्' if not for this way
            if token.find("ङ्\u200d") <= pos and token.find("ङ्\u200d") > -1:
                    pos += 2
            if pos <= l-1:
                #checking for the presence of the  'ः'(.h) matra
                if split[pos] != 'ः':
                    #checking the proximity with the purna-viram
                    if check_proximity(split, pos, t_shlok[i+1]):
                        split.insert(pos, '-')
                        #checking for the presence of half character phonemes near the position where the word
                        #has been split. 
                        if len(split[pos+1]) > 3:
                            print(split[0])
                            print(split[1])
                            print(split[2])
                            print(split[3])
                            print(len(split[pos+1]))
                            print(split[pos])
                            print("here")
                            #here the consonant and the halant are considered as two different characters hence
                            #two characters need to be extracted and appended at the end of the phoneme before the '-'
                            #attaching the two characters to the phoneme before '-'
                            split[pos-1] = split[pos-1] + split[pos+1][0:2]
                            #removing those two characters from the phoneme after '-'
                            split[pos+1] = split[pos+1].replace(split[pos+1][0:2], "")
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