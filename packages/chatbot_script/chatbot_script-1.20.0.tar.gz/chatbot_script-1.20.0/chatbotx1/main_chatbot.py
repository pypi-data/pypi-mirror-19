#!/usr/bin/python3
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
from Female_chatbot import *
from Male_chatbot import *
#from AWNDatabaseManagement import *
#from nltk.corpus import wordnet as wn







def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None

# initialize the connection to the database
sqlite_file = 'DB/brain.sqlite'
connection = sqlite3.connect(sqlite_file)
connection.create_function("REGEXP", 2, regexp)
cursor = connection.cursor()
connection.text_factory = str

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
            connection.commit()
            print(("B:%s" % B)) 
            exit() 
          else:
            B= "اسف!! سوف اعمل على تطوير نفسي"
            print(("B:%s" % B)) 
            exit()
    else:      
          return
  #function for male misunderstanding:
def male_misunderstanding():
     return cursor.execute('SELECT Respond FROM Male_No_Match_Engine ORDER BY RANDOM()').fetchone()

#function for catching the user name:
def findName(Input,Gender):
    if re.search(r'(?:Dr\.|اسمي|انا اسمي|السيدة|انا السيدة|السيد|انا السيد|الانسة|الأنسة)',Input):
       if Gender == 'MALE':
           B = re.sub('^(?:Dr\.|اسمي|انا اسمي|السيدة|انا السيدة|السيد|انا السيد|الانسة|الأنسة)(?P<name>.+)$','تشرفنا اخ\g<name>،', Input) +"كيف استطيع ان اخدمك؟  "
           new_data(Input,B)
           return B
       else: 
           B = re.sub('^(?:Dr\.|اسمي|انا اسمي|السيدة|انا السيدة|السيد|انا السيد|الانسة|الأنسة)(?P<name>.+)$','تشرفنا اخت\g<name>،', Input) +"كيف استطيع ان اخدمك؟  "
           new_data(Input,B)
           return B
    else:
         if Gender == 'MALE':
           B = re.sub('^(?:)(?P<name>.+)$','تشرفنا اخ \g<name>،', Input) +"كيف استطيع ان اخدمك؟  "
           new_data(Input,B)
           return B
         else: 
           B = re.sub('^(?:)(?P<name>.+)$','تشرفنا اخت \g<name>،', Input) +"كيف استطيع ان اخدمك؟  "
           new_data(Input,B)
           return B

#function for catching the user Gender:
def findGender(Input):
    if re.search(r'(?:Dr\.|اسمي|انا اسمي|السيدة|انا السيدة|السيد|انا السيد|الانسة|الأنسة)',Input): 
       N =(re.search('اسمي(.*)', Input).group(1)).strip()
       row =cursor.execute('SELECT Gender FROM Arabic_Names WHERE Name=?',(N,)).fetchone()
       if row:
            if row[0] == 'F':
               gender= 'FEMALE'
            else:
               if row[0] == 'M':
                  gender= 'MALE'
       else:
            G='هل انت ذكر ام انثى؟'
            print(("B:%s" % G))
            H = input('H:')
            if H == 'ذكر':
                gender= 'MALE'
                new_name(N,'M')
            else:
                if H =='انثى':
                   gender= 'FEMALE'
                   new_name(N,'F')
    else:               
          row =cursor.execute('SELECT Gender FROM Arabic_Names WHERE Name=?',(Input,)).fetchone()
          if row:
            if row[0] == 'F':
               gender= 'FEMALE'
            else:
               if row[0] == 'M':
                  gender= 'MALE'
          else:
              G='هل انت ذكر ام انثى؟'
              print(("B:%s" % G))
              H = input('H:')
              if H == 'ذكر':
                  gender= 'MALE'
                  new_name(N,'M')
              else:
                  if H =='انثى':
                     gender= 'FEMALE'
                     new_name(N,'F')            
    return gender                                        
    #-----------------------------------------------#      
#funtion for check the DB:
def check_data(Input):
    row =cursor.execute('SELECT * FROM chatting_log WHERE user=?',(Input,)).fetchone()
    if row:
        return True
    else:
        return False
#funtcion for insert new data:
def new_data(Input,Output):
    row = cursor.execute('SELECT * FROM chatting_log WHERE user=?',(Input,)).fetchone()
    if row:
        return
    else:
        cursor.execute('INSERT INTO chatting_log VALUES (?, ?)', (Input, Output))
        connection.commit()

#funtcion for insert new name:
def new_name(Name,gender):
        cursor.execute('INSERT INTO Arabic_Names VALUES (?, ?)', (Name, gender))
        connection.commit()        
        
#funtcion for Pre_process data:
def PreProcess_text(H):
     tokens=regexp_tokenize(H, r'[،؟!.؛\s+]\s*', gaps=True)
     correct= Autocorrect(tokens)
     return ' '.join(correct)

   #----------------------------------------------# 
B = cursor.execute('SELECT Respond FROM Welcoming_Engine ORDER BY RANDOM()').fetchone()
print(("B:%s" % B))  
H = input('H:')
New_H= PreProcess_text(H)
Check_for_goodbye(New_H)
if len(H) == 0 :
    B= cursor.execute('SELECT Respond FROM Waiting_Engine ORDER BY RANDOM()').fetchone()
    print(("B:%s" % B))
greeting= cursor.execute('SELECT respoce FROM Greeting_Engine WHERE request REGEXP?',[New_H]).fetchone()
if greeting:
    B= greeting[0]
    print(("B:%s" % B))    
    new_data(New_H,B)
H2 = input('H:')
New_H2= PreProcess_text(H2)
gender= findGender(New_H2)  
B = findName(New_H2,gender)
print(("B:%s" % B))
new_data(New_H,B)
if gender == 'MALE':
        connection.close()
        run_conversation_male()
else:
    if gender == 'FEMALE': 
          connection.close()     
          run_conversation_female()
    else:     
          print("ERROR!!")         
           
    
       
   
