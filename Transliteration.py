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
 
#to avoid numbers and punctuation marks
def check_token(token):
    flag = True
    if token == '।' or token == '.':
        flag = False
    elif token.isdigit():
        flag = False
    
    return flag

lang='hi'
language = 'hindi'

tokenizer = TokenizeSentence('sanskrit')
syl = Syllabifier(language)

shlok = u'एवं सततयुक्ता ये भक्तास्त्वां पर्युपासते। येचाप्यक्षरमव्यक्तं तेषां के योगवित्तमाः।।12.1।।'
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
        
#for token in t_shlok:
 #   print(token)

broken = ' '.join(map(str,t_shlok))
print(shlok)
print(broken)
#this is the output of broken
output = u'एवं सत-तयुक्ता ये भक्तास्त्वां प-र्युपासते । येचाप्यक्ष-रमव्यक्तं तेषां के यो-गवित्तमाः । । 12 . 1 । ।'
#how do we pronounce these split words ??
    
#trans_shlok = {ItransTransliterator.to_itrans(word,lang) for word in t_shlok}

#for t_word in trans_shlok:
#    print(t_word)

badi = u'प्रसक्तानी'
#there are minor issues above like badi and chotti matras
#ItransTransliterator.to_itrans(badi, lang)
#'prasaktaanii'
##some manipulation of strings is required