# -*- coding: utf-8 -*-
"""IR_Project_title_body.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Kkj3eaDaPl93otbbVSM7RhWjAlvF85BS

Group 35 \\
Project code
"""

#mounting 
from google.colab import drive
drive.mount('/content/drive')

!pip install contractions

import csv
import nltk
from nltk.corpus import stopwords
import re
from nltk.stem import PorterStemmer
import string
from nltk import word_tokenize
import gensim 
from gensim.models import Word2Vec 
nltk.download('punkt')
nltk.download('wordnet')
nltk.download("stopwords")
import numpy as np
import pandas as pd
import pickle
import contractions
from bs4 import BeautifulSoup
import tensorflow as tf
import tensorflow_hub as hub
import ast
import joblib

stop_words = stopwords.words('english')

def preprocessingQT(text):
  #convert to lowercase
  text = text.lower()
  #expand contractions
  text = contractions.fix(text)
  text = text.replace("?"," ?")
  #split to tokens
  text = text.split()
  #stopward removal 
  words = [ w for w in text if not w in stop_words]
  sentence  = ' '.join(words)
  return sentence

def preprocessingQB(text):
  #convert to lowercase
  text = text.lower()
  #expand contractions
  text = contractions.fix(text)
  #replace \n with space
  text = re.sub("\n"," ", text)
  #replace quotes with space
  text = re.sub("[\"\']"," ", text)
  #replace codeblocks with space.
  text = re.sub("<pre><code>[A-A a-z 0-9 !\"#$%&\\'()*+,-./:;<=>?@[\\]^_`{|}~]*</code></pre>"," ",text);
  #remove remaining tags.
  soup = BeautifulSoup(text)
  text = soup.get_text()
  #split to tokens
  text = text.split()
  #stopward removal
  words =[ w for w in text if not w in stop_words]
  sentence  = ' '.join(words)
  return sentence

original=[]
changed = []
def savePreproccessedData():
  with open('/content/drive/MyDrive/IR project/archive/Questions.csv', encoding="latin1") as csvfile ,open('/content/drive/MyDrive/IR project/archive/finalOutput.csv' ,'w' ,newline='') as myfile:
    readCSV = csv.reader(csvfile, delimiter=',' )
    writeCSV = csv.writer(myfile , delimiter = ',')
    next(readCSV, None) 
    for row in readCSV:
      doc_id = row[0];
      title = row[5];
      body = row[6];
      data = title+" "+ body
      p_title = preprocessingQT(title)
      p_body = preprocessingQB(body)
      p_data = p_title+" "+p_body
      original.append(data)
      changed.append(p_data)
      writeCSV.writerow((doc_id, p_data))

#Preprocessing the corpus and storing in new file.
savePreproccessedData()

#loading the universal sentence encoder model
use_embeddings = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

#function to create the sentence embeddings and store in a csv file.
def createEmbeddings():
  with open('/content/drive/MyDrive/IR project/archive/finalOutput.csv', encoding="latin1") as csvfile, open('/content/drive/MyDrive/IR project/sentenceEmbeddings.csv' ,'w' ,newline='') as myfile:
    readCsv = csv.reader(csvfile, delimiter=',' )
    writeCSV = csv.writer(myfile, delimiter = ',')
    for row in readCsv:
      id = row[0]
      ques = row[1]
      ques_list = [ques]
      sent_tfTensor = use_embeddings(ques_list)
      array_embeddings = tf.make_ndarray(tf.make_tensor_proto(sent_tfTensor))
      list_embeddings = array_embeddings.tolist()[0]
      writeCSV.writerow((id, list_embeddings))

createEmbeddings()

def getTitleList():
  titledict = {}
  with open('/content/drive/MyDrive/IR project/Questions.csv', encoding="latin1") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',' )
    next(readCSV, None) 
    for row in readCSV:
      title = row[5];
      titledict[row[0]] = title
  return titledict

titledict = getTitleList()

len(titledict)

#opening the csv file 
filename = open("/content/drive/MyDrive/IR project/sentenceEmbeddings.csv", 'r')  
# creating dictreader object with col names
file = csv.DictReader(filename, fieldnames=['id', 'vector'])

idlist= []
embeddings = []
for col in file:
  embeddings.append(np.array(ast.literal_eval(col['vector'])))
  idlist.append(col['id'])

embeddings = np.array(embeddings)    
joblib.dump(embeddings,"/content/drive/MyDrive/IR project/embeddings_9may" )

import joblib
joblib.dump(embeddings,"/content/drive/MyDrive/IR project/embeddings_8may_sakshi_full" )

joblib.dump(idlist,"/content/drive/MyDrive/IR project/ids_8may_full" )

import joblib
joblib.dump(idlist,"/content/drive/MyDrive/IR project/id_5may_sakshi_full" )

joblib.dump(embeddings,"/content/drive/MyDrive/IR project/embeddings_5may_sakshi_title_body_full" )

#count = 442649
joblib.dump(idlist,"/content/drive/MyDrive/IR project/id_5may_sakshi_title_body" )

joblib.dump(embeddings,"/content/drive/MyDrive/IR project/embedding_5may_sakshi_title_body" )
#joblib.dump(idlist,"/content/drive/MyDrive/IR project/id_5may_sakshi_title_body" )

joblib.dump(embeddings,"/content/drive/MyDrive/IR project/embeddingList1" )

embeddings = joblib.load("/content/drive/MyDrive/IR project/embeddings_8may_sakshi_full")

ids = joblib.load("/content/drive/MyDrive/IR project/id_5may_sakshi_full")

len(ids)

idlist = ids

from scipy.spatial import distance
def calCosSim(test_query_embedding, embeddings, idlist):
  test_query_embeddingArr = np.array(test_query_embedding)
  #embeddingsArr = np.array(embeddings)
  embeddingsArr = embeddings
  result = distance.cdist(test_query_embeddingArr, embeddingsArr, "cosine")
  final_res = 1-result[0]
  final_list = list(zip(final_res, idlist))
  final_list.sort(reverse=True)
  return final_list

queries = ['insert query in sql table', 'tags in html and css', 'concatenate a string in C#', 'install pip in python' ,'append element in list in python']
for query in queries:
  processed_test_query = preprocessingQT(query)
  print("query: ", query)
  sent_tfTensor = use_embeddings([processed_test_query])
  array_embeddings = tf.make_ndarray(tf.make_tensor_proto(sent_tfTensor))
  test_query_embeddings  = array_embeddings.tolist()
  #print(test_query_embeddings)
  final_list = calCosSim(test_query_embeddings, embeddings, idlist)
  print("relevant result with score:")
  for f in final_list[:10]:
    print(f[0]," : ", titledict[f[1]])
  print("\n")

#keyword based searching
#function to extract the preprocessed queries.
p_ques = []
def createprocessedList():
  with open('/content/drive/MyDrive/IR project/archive/finalOutput.csv', encoding="latin1") as csvfile:
    readCsv = csv.reader(csvfile, delimiter=',' )
    for row in readCsv:
      ques = row[1]
      p_ques.append(ques)

createprocessedList()

len(p_ques)

from sklearn.feature_extraction.text import TfidfVectorizer
def tfidfModel(sentences):
  tfidf_model = TfidfVectorizer(use_idf=True)
  tfidf_model_vectors = tfidf_model.fit(sentences)
  word_Tfidf_Dict = dict(zip(tfidf_model_vectors.get_feature_names(), list(tfidf_model_vectors.idf_)))
  tfidf_features = tfidf_model_vectors.get_feature_names()
  return word_Tfidf_Dict, tfidf_features

dictionary, features = tfidfModel(p_ques[:100000])

def tfidfScoring(sentences, dictionary, features, query,idlist):
  tf_idf_score_query = []
  words = query.split()
  for sent in sentences:
    tf_idf_score_sum = 0 
    wordlist = sent.split(" ")
    for word in words:
      if word in wordlist and word in features:
          tf_idf_score = dictionary[word]*(wordlist.count(word)/len(wordlist))
          tf_idf_score_sum += tf_idf_score 
    tf_idf_score_query.append(tf_idf_score_sum)
  final_list = list(zip( tf_idf_score_query, idlist))
  final_list.sort(reverse=True)
  return final_list

queries = ['insert query in sql table' ]
for query in queries:
  processed_test_query = preprocessingQT(query)
  print("query: ", query)
  final_list = tfidfScoring(p_ques[:100000], dictionary, features, processed_test_query, idlist[:100000])
  print("relevant result with score:")
  for f in final_list[:10]:
    print(f[0]," : ", titledict[f[1]])
  print("\n")

