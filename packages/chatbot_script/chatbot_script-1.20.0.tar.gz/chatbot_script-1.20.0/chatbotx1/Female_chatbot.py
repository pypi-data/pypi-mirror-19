# -*- coding: utf-8 -*-
import re,string,sys
import sqlite3
import codecs
import types
import nltk
from nltk import pos_tag
from nltk.tokenize import  regexp_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem.isri import ISRIStemmer
from arabic_const import *
from normalize import *
from stemming import *
from nltk.tag.stanford import StanfordPOSTagger
from ar_ghalat import *
#from AWNDatabaseManagement import *
#from nltk.corpus import wordnet as wn




def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None

# initialize the connection to the main_database
sqlite_main = 'DB/brain.sqlite'
conn = sqlite3.connect(sqlite_main)
conn.create_function("REGEXP", 2, regexp)
cursor = conn.cursor()
conn.text_factory = str


st=ArabicLightStemmer()
arb_model_filename = '/Users/emansaad/Desktop/chatbot1/stanford-postagger-full-2015-04-20/models/arabic.tagger'
my_path_to_jar = '/Users/emansaad/Desktop/chatbot1/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
Stop_list = [x[0] for x in cursor.execute('SELECT Stop_word FROM Stop_Words').fetchall()]
   #-----------------------------------------------#
sent_data = cursor.execute('SELECT word,state FROM train_words').fetchall()  
all_words1 = set(word.lower() for passage in sent_data for word in word_tokenize(passage[0]))
t1 = [({word: (word in word_tokenize(x[0])) for word in all_words1}, x[1]) for x in sent_data]
  #-----------------------------------------------#
#function for goodbye:  
def Check_for_goodbye(Input):
    if re.search(r'باي|الى اللقاء',Input):
          B ='تقييمك لعملي؟'
          print(("B:%s" % B)) 
          H2 = input('H:')
          classifier1 = nltk.NaiveBayesClassifier.train(t1)
          test_sent_features = {word.lower(): (word in word_tokenize(H2)) for word in all_words1}
          sent_result= classifier1.classify(test_sent_features)
          if sent_result == 'Positive':
            B= cursor.execute('SELECT Respond FROM Goodbye_Engine ORDER BY RANDOM()').fetchone()
            cursor.execute('DELETE FROM chatting_log')
            conn.commit()
            print(("B:%s" % B)) 
            exit() 
          else:
            B= "اسف!! سوف اعمل على تطوير نفسي"
            print(("B:%s" % B)) 
            exit()
    else:      
          return       
#function for female misunderstanding:
def female_misunderstanding():
     return cursor.execute('SELECT Respond FROM Female_No_Match_Engine ORDER BY RANDOM()').fetchone()          

#--------------------------------------------# 
#function for finding the pronoun:
def find_pronoun(input):
     pronoun = []
     for w,t in input:
         if t in ('PRP'):
            pronoun.append(w)   
     return pronoun       
#function for finding the noun:
def find_noun(input):
     noun = []
     for w,t in input:
         if t in ('NN','NNS','NNP','NNPS', 'DTNN'):
             noun.append(w) 
     return noun
#function for finding the adjective:
def find_adjective(input):
     adjective = []
     for w,t in input:
         if t in ('JJ','JJR','JJS','DTJJ'):
             adjective.append(w) 
     return adjective
#function for finding the verb:
def find_verb(input):
     verb = []
     for w,t in input:
         if t in('VB','VBD','VBG','VBN','VBP','VBZ'):
             verb.append(w) 
     return verb 
#--------------------------------------------#
#function for removing stop words:
def Remove_StopWords(Input):
         Free=[]
         for w in Input:
             if w not in Stop_list:
                 Free.append(w)    
         return Free
#function for Normlization:
def normlization(text):
    norm_text=[]
    for w in text:
	    text= strip_tashkeel(strip_tatweel(normalize_lamalef(normalize_hamza(w))))
	    norm_text.append(text)
    return norm_text
#function for tagging the words:
def tagging(Input):
    Arabic_postagger = StanfordPOSTagger(model_filename=arb_model_filename, path_to_jar=my_path_to_jar)
    Arabic_postagger._SEPARATOR = '/'
    tagg=Arabic_postagger.tag(Input) 
    return tagg 
     #Pnoun= find_pronoun(tagg)
     #noun= find_noun(tagg)
     #adjective= find_adjective(tagg)
     #verb= find_verb(tagg) 
     #return Pnoun,noun,adjective,verb
# function for Autocorrect:
def Autocorrect(Input):
    correct=[]
    for c in Input:
         correct.append(autocorrectlist(c))
    return correct 
#function for Stemming words:
def Stemming1(Input):
    st=ArabicLightStemmer()
    stem=[]
    for w,t in Input:
       if t in ('NN','NNS','NNP','NNPS', 'DTNN', 'DTNNS','JJ','JJR','JJS','DTJJ'):
             stem.append(w)
       else:     
             stem.append(st.lightStem(w))
    return stem
#function for Stemming words:
def Stemming2(Input):
    stt=ArabicLightStemmer()
    stem=[]
    for w in Input:
        stem.append(stt.lightStem(w))
    return stem 
#function for PreProcessing:
def PreProcess_text(Input):
    tokens=regexp_tokenize(Input, r'[،؟!.؛\s+]\s*', gaps=True)
    Free= Remove_StopWords(normlization(tokens))
    correct= Autocorrect(Free)
    tag= tagging(correct)
    Steem = Stemming1(tag)
    return Steem                            
    #-----------------------------------------------#      
#funtion for check the DB:
def check_data(Input):
    row =cursor.execute('SELECT * FROM chatting_log WHERE user=?',(Input,)).fetchone()
    if row:
        return True
    else:
        return False
#funtcion for insert conv logs:
def new_data(Input,Output):
    row = cursor.execute('SELECT * FROM chatting_log WHERE user=?',(Input,)).fetchone()
    if row:
        return
    else:
        cursor.execute('INSERT INTO chatting_log VALUES (?, ?)', (Input, Output))
        conn.commit()
#funtcion for learn new data:
def learn(Input,Output):
        cursor.execute('INSERT INTO Female_Conversation_Engine VALUES (?, ?)', (Input, Output))
        B='حسناً..شكراً لك عزيزتي'
        print(("B:%s" % B)) 
        conn.commit()
        
        
#function for txt synom : 
def check_synonym(text):
    find= "False"
    tokens=regexp_tokenize(text, r'[،؟!.؛\s+]\s*', gaps=True)
    main=cursor.execute('SELECT request FROM Female_Conversation_Engine WHERE request REGEXP?',[tokens[0]]).fetchone()
    if main: 
        based_text= ' '.join(main)
        based_tokens=regexp_tokenize(str(based_text), r'[،؟!.؛\s+]\s*', gaps=True)
        s1 = set(tokens)
        s2 = set(based_tokens)
        for w1,w2 in zip(s1,s2):
            if w1==w2:
                tokens.remove(w1),based_tokens.remove(w2) 
        if len(tokens)== 1 and len(based_tokens)== 1:
             Steem1 = ' '.join(Stemming2(tokens))
             Steem2 = ' '.join(Stemming2(based_tokens))
             if Steem1 == Steem2:
                 return based_text
             else:    
                Diff1= ' '.join(cursor.execute('SELECT definition FROM Arabic_Dic WHERE Word REGEXP?',[Steem1]).fetchone())
                Diff2= ' '.join(cursor.execute('SELECT definition FROM Arabic_Dic WHERE Word REGEXP?',[Steem2]).fetchone())      
                for D in Diff1:
                 if D in Diff2:
                    return based_text
                 else:
                     return find     
        else:
            return find               
    else:
        return find
   #----------------------------------------------#  
def run_conversation_female():  
       while True:  
           H = input('H:')
           B= Check_for_goodbye(H)
           if len(H) == 0 :
              B= cursor.execute('SELECT Respond FROM Female_Waiting_Engine ORDER BY RANDOM()').fetchone()
              print(("B:%s" % B))
              continue
           New_H= ' '.join(PreProcess_text(H))
           if check_data(H) == True:
              B="نعم اعرف ذلك!!"
              print(("B:%s" % B))
              continue    
           reply= cursor.execute('SELECT respoce FROM Female_Conversation_Engine WHERE request REGEXP?',[New_H]).fetchone()
           if reply:
              B=reply[0]
              print(("B:%s" % B))
              new_data(H,B)
              continue
           else:     
              check= check_synonym(H)
              if check == False :
                  B= female_misunderstanding()
                  print(("B:%s" % B))
              else:
                reply_new= cursor.execute('SELECT respoce FROM Female_Conversation_Engine WHERE request REGEXP?',[check]).fetchone()
                if reply_new:
                    B=reply_new[0]
                    print(("B:%s" % B))
                    new_data(check,B)
                    cursor.execute('INSERT INTO Female_Conversation_Engine VALUES (?, ?)', (H, B))
                    conn.commit()
                    continue
                else:    
                     B= female_misunderstanding()
                     print(("B:%s" % B))
                
           
    
       
   
