#!/usr/bin/python
# -*- coding=utf-8 -*-
#************************************************************************
# $Id: ar_ghalat.py,v 0.7 2009/06/02 01:10:00 Taha Zerrouki $
#
# ------------
# Description:
# ------------
#  Copyright (c) 2011, Arabtechies, Arabeyes Taha Zerrouki
#
#  Elementary function to detect and correct minor spell error for  arabic texte
#
# -----------------
# Revision Details:    (Updated by Revision Control System)
# -----------------
#  $Date: 2011/01/05 01:10:00 $
#  $Author: Taha Zerrouki $
#  $Revision: 0.1 $
#  $Source: arabtechies.sourceforge.net
#
#***********************************************************************/

import re, string,sys
import types
from arabic_const import *
from ar_autocorrectlist import *

import re
replacement_table=[
# removing kashida (Tatweel)
(re.compile(r'([\u0621-\u063F\u0641-\u064A])\u0640+([\u0621-\u063F\u0641-\u064A])',re.UNICODE), r'\1\2'), 
# rules for انفعال
(re.compile(r'\b(و|ف|)(ك|ب|)(ال|)إن(\w\w)ا(\w)(ي|)(ين|ات|ة|تين|)\b',re.UNICODE), r'\1\2\3ان\4ا\5\6\7'),
(re.compile(r'\b(و|ف|)(لل|)إن(\w\w)ا(\w)(ي|)(ين|ات|تين|ة|)\b',re.UNICODE), r'\1\2ان\3ا\4\5\6'),
(re.compile(r'\b(و|ف|)(ك|ب|ل|)إن(\w\w)ا(\w)(ي|)(هما|كما|هم|كم|هن|كن|نا|ه|ك|ها|تهما|تكما|تهم|تكم|تهن|تكن|تنا|ته|تها|تك|اتهما|اتكما|اتهم|اتكم|اتهن|اتكن|اتنا|اته|اتها|اتك|)\b',re.UNICODE), r'\1\2ان\3ا\4\5\6'),
(re.compile(r'\b(و|ف|)(ال|)إن(\w\w)ا(\w)(ي|)(ين|ان|تين|تان|ون|)\b',re.UNICODE), r'\1\2ان\3ا\4\5\6'),
(re.compile(r'\b(و|ف|)إن(\w\w)ا(\w)(ي|)(ًا|اً|ا|)\b',re.UNICODE), r'\1ان\2ا\3\4\5'),
# rules for افتعال
(re.compile(r'\b(و|ف|)(ك|ب|)(ال|)إ(\w)ت(\w)ا(\w)(ي|)(ين|ات|ة|تين|)\b',re.UNICODE), r'\1\2\3ا\4ت\5ا\6\7\8'),
(re.compile(r'\b(و|ف|)(لل|)إ(\w)ت(\w)ا(\w)(ي|)(ين|ات|تين|ة|)\b',re.UNICODE), r'\1\2ا\3ت\4ا\5\6\7'),
(re.compile(r'\b(و|ف|)(ك|ب|ل|)إ(\w)ت(\w)ا(\w)(ي|)(هما|كما|هم|كم|هن|كن|نا|ه|ك|ها|تهما|تكما|تهم|تكم|تهن|تكن|تنا|ته|تها|تك|اتهما|اتكما|اتهم|اتكم|اتهن|اتكن|اتنا|اته|اتها|اتك|)\b',re.UNICODE), r'\1\2ا\3ت\4ا\5\6\7'),
(re.compile(r'\b(و|ف|)(ال|)إ(\w)ت(\w)ا(\w)(ي|)(ين|ان|تين|تان|ون|)\b',re.UNICODE), r'\1\2ا\3ت\4ا\5\6\7'),
(re.compile(r'\b(و|ف|)إ(\w)ت(\w)ا(\w)(ي|)(ًا|اً|ا|)\b',re.UNICODE), r'\1ا\2ت\3ا\4\5\6'),
# rules for افتعال التي تحوي ضط أو صط أو زد
(re.compile(r'\b(و|ف|)(ك|ب|)(ال|)إ(زد|ضط|صط)(\w)ا(\w)(ي|)(ين|ات|ة|تين|)\b',re.UNICODE), r'\1\2\3ا\4\5ا\6\7\8'),
(re.compile(r'\b(و|ف|)(لل|)إ(ﺯﺩ|ﺾﻃ|ﺺﻃ)(\w)ا(\w)(ي|)(ين|ات|تين|ة|)\b',re.UNICODE), r'\1\2ا\3\4ا\5\6\7'),
(re.compile(r'\b(و|ف|)(ك|ب|ل|)إ(ﺯﺩ|ﺾﻃ|ﺺﻃ)(\w)ا(\w)(ي|)(هما|كما|هم|كم|هن|كن|نا|ه|ك|ها|تهما|تكما|تهم|تكم|تهن|تكن|تنا|ته|تها|تك|اتهما|اتكما|اتهم|اتكم|اتهن|اتكن|اتنا|اته|اتها|اتك|)\b',re.UNICODE), r'\1\2ا\3\4ا\5\6\7'),
(re.compile(r'\b(و|ف|)(ال|)إ(ﺯﺩ|ﺾﻃ|ﺺﻃ)(\w)ا(\w)(ي|)(ين|ان|تين|تان|ون|)\b',re.UNICODE), r'\1\2ا\3\4ا\5\6\7'),
(re.compile(r'\b(و|ف|)إ(ﺯﺩ|ﺾﻃ|ﺺﻃ)(\w)ا(\w)(ي|)(ًا|اً|ا|)\b',re.UNICODE), r'\1ا\2\3ا\4\5\6'),
# حالة الألف المقصورة بعدها همزة في آخر الكلمة، وعادة مايكون البديل همزة على النبرة. 
(re.compile(r'ىء\b',re.UNICODE), r'ئ'),
# حالة الألف المقصورة ليست في آخر الكلمة، وعادة مايوضع بعدها فراغ 
(re.compile(r'ى([^ء]+)\b',re.UNICODE), r'ى \1'),
# حالة التاء المربوطة ليست في آخر الكلمة، وعادة مايوضع بعدها فراغ 
(re.compile(r'ة(\w+)\b',re.UNICODE), r'ة \1'),
# حالة الالف المكررة بعدها لام،يكون البديل بين اﻷلفين فراغ 
(re.compile(r'\bاال(\w+)\b',re.UNICODE), r'ال\1'),
(re.compile(r'(\w+)اال(\w+)\b',re.UNICODE), r'\1ا ال\2'),
(re.compile(r'(\w+)(ا+)(\w+)\b',re.UNICODE), r'\1ا\3'),
(re.compile(r'ا(ا+)',re.UNICODE), r'ا'),
]


def is_valid_arabic_word(word):
    if len(word)==0: return False;
    word_nm=ar_strip_marks_keepshadda(word);
    # the alef_madda is  considered as 2 letters
    word_nm=word_nm.replace(ALEF_MADDA,HAMZA+ALEF);
    if word[0] in (WAW_HAMZA,YEH_HAMZA,FATHA,DAMMA,SUKUN,KASRA):
        return False;
#  إذا كانت الألف المقصورة في غير آخر الفعل
    if re.match("^(.)*[%s](.)+$"%ALEF_MAKSURA,word):
        return False;
#  إذا كانت الألف المقصورة في غير آخر الفعل		
    if re.match("^(.)*[%s]([^%s%s%s])(.)+$"%(TEH_MARBUTA,DAMMA,KASRA,FATHA),word):
        return False;
##    i=0;

    if re.search("([^\u0621-\u0652%s%s%s])"%(LAM_ALEF, LAM_ALEF_HAMZA_ABOVE,LAM_ALEF_MADDA_ABOVE),word):
        return False;
    if re.match("([\d])+",word):
        return False;
    return True;
	
	
def autocorrectlist(word):
	# autocorrect words from a list 
	# autocorrect words without diacritics 
	
	if word in autocorrect_arabic_list:
		return autocorrect_arabic_list[word];
	else: 
		return word
	
def validate_word_list(word_list, show_correct=False):
	for word in word_list:
		valid=is_valid_arabic_word(word);
		if not valid:
			print(("\t".join([word,str(valid)])).encode('utf8'));

		result=autocorrectlist(word);
		if result:
			print("\t#".join([word,result]).encode('utf-8'));		
		else: # if the word isn't in the autolist, use regular expression
			result=autocorrect(word);
			if result:
				print("\t*".join([word,result]).encode('utf-8'));
			else:
				if show_correct:
					print("\t".join([word]).encode('utf-8'));


