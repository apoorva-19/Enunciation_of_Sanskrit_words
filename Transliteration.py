#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 22:01:41 2018

@author: apoorva
"""
##to run you first need to install cltk
##pip install cltk

from cltk.corpus.sanskrit.itrans.unicode_transliterate import ItransTransliterator
from cltk.tokenize.sentence import TokenizeSentence
from cltk.stem.sanskrit.indian_syllabifier import Syllabifier

lang='hi'
language = 'hindi'
tokenizer = TokenizeSentence('sanskrit')
syl = Syllabifier(language)
 
if __name__ == '__main__':
	import sys
	
if len(sys.argv) == 1:
	print ('Needs filename for splitting shlokas');
	sys.exit(-1)
elif len(sys.argv) == 2:
	print ('Needs filename for storing split shlokas');
	sys.exit(-1)
	
#to avoid numbers and punctuation marks
def check_token(token):
    flag = True
    if token == '।' or token == '.':
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
	
#shlok = u'एवं सततयुक्ता ये भक्तास्त्वां पर्युपासते। येचाप्यक्षरमव्यक्तं तेषां के योगवित्तमाः।।12.1।।'
for shlok in filestring:
	t_shlok = tokenizer.tokenize(shlok)
	
	#splitiing the words in anushthup format
	count = 0
	for i in range(len(t_shlok)):
		token = t_shlok[i]
		split = syl.orthographic_syllabify(token)
		l = len(split)
		if(l < 4 and check_token(token)):
		    count = count + l
		elif(l > 4 and check_token(token)):
		    diff = l - (4-count)
		    split.insert(4-count, '-')
		    t_shlok[i] = ''.join(map(str, split))
		    count = diff
		if count%4 == 0 or l == 4:
		    count = 0
		    
	broken = ' '.join(map(str,t_shlok))
	outfile.write(broken + "\n")
	
outfile.close()
    
#trans_shlok = {ItransTransliterator.to_itrans(word,lang) for word in t_shlok}

#for t_word in trans_shlok:
#    print(t_word)

