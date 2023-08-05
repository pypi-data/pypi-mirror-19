#!/usr/bin/python
# -*- coding=utf-8 -*-
"""
Utility functions used by to prepare an arabic text to search and index .
"""
import re, string,sys
from arabic_const import *


HARAKAT_pat =re.compile(r"["+"".join([FATHATAN,DAMMATAN,KASRATAN,FATHA,DAMMA,KASRA,SUKUN,SHADDA])+"]")
HAMZAT_pat =re.compile(r"["+"".join([WAW_HAMZA,YEH_HAMZA])+"]");
ALEFAT_pat =re.compile(r"["+"".join([ALEF_MADDA,ALEF_HAMZA_ABOVE,ALEF_HAMZA_BELOW,HAMZA_ABOVE,HAMZA_BELOW])+"]");
LAMALEFAT_pat =re.compile(r"["+"".join([LAM_ALEF,LAM_ALEF_HAMZA_ABOVE,LAM_ALEF_HAMZA_BELOW,LAM_ALEF_MADDA_ABOVE])+"]");

######################################################################
#{ Indivudual Functions
######################################################################

#--------------------------------------
def strip_tashkeel(text):
	"""Strip vowel from a text and return a result text.
	The striped marks are : 
		- FATHA, DAMMA, KASRA
		- SUKUN
		- SHADDA
		- FATHATAN, DAMMATAN, KASRATAN, , , .
	Example:
		>>> text=u"الْعَرَبِيّةُ"
		>>> strip_tashkeel(text)
		العربية

	@param text: arabic text.
	@type text: unicode.
	@return: return a striped text.
	@rtype: unicode.
    """
	return HARAKAT_pat.sub('', text)


#strip tatweel from a text and return a result text
#--------------------------------------
def strip_tatweel(text):
	"""
	Strip tatweel from a text and return a result text.

	Example:
		>>> text=u"العـــــربية"
		>>> strip_tatweel(text)
		العربية

	@param text: arabic text.
	@type text: unicode.
	@return: return a striped text.
	@rtype: unicode.
	"""
	return re.sub(r'[%s]' % TATWEEL,	'', text)


#--------------------------------------
def normalize_hamza(text):
	"""Normalize Hamza forms into one form, and return a result text.
	The converted letters are : 
		- The converted lettersinto HAMZA are: WAW_HAMZA,YEH_HAMZA 
		- The converted lettersinto ALEF are: ALEF_MADDA, ALEF_HAMZA_ABOVE, ALEF_HAMZA_BELOW ,HAMZA_ABOVE, HAMZA_BELOW 

	Example:
		>>> text=u"أهؤلاء من أولئكُ"
		>>> normalize_hamza(text)
		اهءلاء من اولءكُ

	@param text: arabic text.
	@type text: unicode.
	@return: return a converted text.
	@rtype: unicode.
    """
	text=ALEFAT_pat.sub(ALEF, text)
	return HAMZAT_pat.sub(HAMZA, text)

#--------------------------------------
def normalize_lamalef(text):
	"""Normalize Lam Alef ligatures into two letters (LAM and ALEF), and Tand return a result text.
	Some systems present lamAlef ligature as a single letter, this function convert it into two letters,
	The converted letters into  LAM and ALEF are : 
		- LAM_ALEF, LAM_ALEF_HAMZA_ABOVE, LAM_ALEF_HAMZA_BELOW, LAM_ALEF_MADDA_ABOVE

	Example:
		>>> text=u"لانها لالء الاسلام"
		>>> normalize_lamalef(text)
		لانها لالئ الاسلام

	@param text: arabic text.
	@type text: unicode.
	@return: return a converted text.
	@rtype: unicode.
	"""
	return LAMALEFAT_pat.sub('%s%s'%(LAM,ALEF), text)

#--------------------------------------
def normalize_spellerrors(text):
	"""Normalize some spellerrors like, TEH_MARBUTA into HEH,ALEF_MAKSURA into YEH, and Tand return a result text.
	In some context users omit the difference between TEH_MARBUTA and HEH, and ALEF_MAKSURA and YEh.
	The conversions are:
		- TEH_MARBUTA into HEH
		- ALEF_MAKSURA into YEH

	Example:
		>>> text=u"اشترت سلمى دمية وحلوى"
		>>> normalize_spellerrors(text)
		اشترت سلمي دميه وحلوي

	@param text: arabic text.
	@type text: unicode.
	@return: return a converted text.
	@rtype: unicode. 
	"""
	text=re.sub(r'[%s]' % TEH_MARBUTA,	HEH, text)
	return re.sub(r'[%s]' % ALEF_MAKSURA,	YEH, text)
