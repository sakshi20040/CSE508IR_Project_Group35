import json
import sys
import time
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import csv
import numpy
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download("stopwords")
from nltk.corpus import stopwords
import re
from nltk.stem import PorterStemmer
import string
from nltk import word_tokenize
import numpy as np
import contractions
from bs4 import BeautifulSoup
import tensorflow as tf
import tensorflow_hub as hub
import joblib
from scipy.spatial import distance
from pywebio.input import *
from pywebio.output import *
import googletrans
from pywebio import start_server
from googletrans import Translator

stop_words=stopwords.words('english')
stemming = PorterStemmer()
translator = Translator()


def ESconnection():
    es = Elasticsearch([{"host": "localhost", "port": 9200}])
    if es.ping():
            print("connected to elastic search")
    else:
            print("not connected to elastic search")
            sys.exit()
    return es

def preprocessingQT(text):
  #convert to lowercase
  text = text.lower()
  #expand contractions
  text = contractions.fix(text)
  text = text.replace("?"," ?")
  #split to tokens
  text = text.split()
  #stopward removal
  words = [stemming.stem(w) for w in text if not w in stop_words]
  sentence  = ' '.join(words)
  return sentence

def keywordBasedSearching(es, ques):
    body = {
            'query':{
                'match':{
                    "title" : ques
                }
            }
        }
    res = es.search(index='question_bank',body=body)
    return res


def calCosSim(test_query_embedding, embeddings, idlist):
  test_query_embeddingArr = np.array(test_query_embedding)
  embeddingsArr = embeddings
  result = distance.cdist(test_query_embeddingArr, embeddingsArr, "cosine")
  final_res = 1-result[0]
  final_list = list(zip(final_res, idlist))
  final_list.sort(reverse=True)
  final_list = final_list[:10]
  return final_list

def saveAnswers():
  ans_dict = {}
  with open('Answers.csv', encoding="latin1") as csvfile:
    readCsv = csv.reader(csvfile, delimiter=',' )
    next(readCsv, None)
    for row in readCsv:
      id = row[3]
      score = row[4]
      body =  row[5]
      t = (score, body)
      if not id in ans_dict:
        ans_dict[id] = list()
      ans_dict[id].append(t)
  csvfile.close()
  final_ans_dict = {}
  for id, score_body_tuple in ans_dict.items():
    score = score_body_tuple[0][0]
    body = score_body_tuple[0][1]
    for i in range(1,len(score_body_tuple)):
      if(int(score) < int(score_body_tuple[i][0])):
        score = score_body_tuple[i][0]
        body = score_body_tuple[i][1]
    final_ans_dict[id] = body
  ans_dict = {}
  return final_ans_dict

def getTitleList():
  titledict = {}
  with open('Questions.csv', encoding="latin1") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',' )
    next(readCSV, None)
    for row in readCSV:
      title = row[5];
      titledict[row[0]] = title
    csvfile.close()
  return titledict



def showtext0():
    if final_ids[0] in ansdict:
    	ans = ansdict[final_ids[0]]
    else:
    	ans = '<p>No answer available ...</p>'	
    popup('Result', [
    put_html('<p>'+titledict[final_ids[0]]+'</p>\n'+ans),
    put_buttons(['Close'], onclick=lambda _: close_popup())
	])
	
def showtext1():
    if final_ids[1] in ansdict:
    	ans = ansdict[final_ids[1]]
    else:
    	ans = '<p>No answer available ...</p>'
    popup('Result', [
    put_html('<p>'+titledict[final_ids[1]]+'</p>\n'+ans),
    put_buttons(['Close'], onclick=lambda _: close_popup())
	])
	
def showtext2():
    if final_ids[2] in ansdict:
    	ans = ansdict[final_ids[2]]
    else:
    	ans = '<p>No answer available ...</p>'
    popup('Result', [
    put_html('<p>'+titledict[final_ids[2]]+'</p>\n'+ans),
    put_buttons(['Close'], onclick=lambda _: close_popup())
	])
def showtext3():
    if final_ids[3] in ansdict:
    	ans = ansdict[final_ids[3]]
    else:
    	ans = '<p>No answer available ...</p>'
    popup('Result', [
    put_html('<p>'+titledict[final_ids[3]]+'</p>\n'+ans),
    put_buttons(['Close'], onclick=lambda _: close_popup())
	])
def showtext4():
    if final_ids[4] in ansdict:
    	ans = ansdict[final_ids[4]]
    else:
    	ans = '<p>No answer available ...</p>'
    popup('Result', [
    put_html('<p>'+titledict[final_ids[4]]+'</p>\n'+ans),
    put_buttons(['Close'], onclick=lambda _: close_popup())
	])
def showtext5():
    if final_ids[5] in ansdict:
    	ans = ansdict[final_ids[5]]
    else:
    	ans = '<p>No answer available ...</p>'
    popup('Result', [
    put_html('<p>'+titledict[final_ids[5]]+'</p>\n'+ans),
    put_buttons(['Close'], onclick=lambda _: close_popup())
	])
def showtext6():
    if final_ids[6] in ansdict:
    	ans = ansdict[final_ids[6]]
    else:
    	ans = '<p>No answer available ...</p>'
    popup('Result', [
    put_html('<p>'+titledict[final_ids[6]]+'</p>\n'+ans),
    put_buttons(['Close'], onclick=lambda _: close_popup())
	])
def showtext7():
    if final_ids[7] in ansdict:
    	ans = ansdict[final_ids[7]]
    else:
    	ans = '<p>No answer available ...</p>'
    popup('Result', [
    put_html('<p>'+titledict[final_ids[7]]+'</p>\n'+ans),
    put_buttons(['Close'], onclick=lambda _: close_popup())
	])

def showtext8():
    if final_ids[8] in ansdict:
    	ans = ansdict[final_ids[8]]
    else:
    	ans = '<p>No answer available ...</p>'
    popup('Result', [
    put_html('<p>'+titledict[final_ids[8]]+'</p>\n'+ans),
    put_buttons(['Close'], onclick=lambda _: close_popup())
	])

def showtext9():
    if final_ids[9] in ansdict:
    	ans = ansdict[final_ids[9]]
    else:
    	ans = '<\p>No answer available ...</p>'
    popup('Result', [
    put_html('<p>'+titledict[final_ids[9]]+'</p>\n'+ans),
    put_buttons(['Close'], onclick=lambda _: close_popup())
	])

titledict = getTitleList()
print("title done")
ansdict = saveAnswers()
print("ans done")
final_scores =[]
final_ids = []

#embeddings = joblib.load( "embeddings_8may_sakshi_full" )
#embeddings = embeddings[:1000000]
embeddings = joblib.load("embeddingList1_soumam_testing_with_title_only")
print(" emb loaded", len(embeddings))
idlist = joblib.load("ids_8may_full")
idlist = idlist[:200000]
print("id loaded", len(idlist))
#loading the universal sentence encoder model
use_embeddings = hub.load("universal-sentence-encoder_4")
print("use emb loaded")
print("loaded all")

def app():
	es = ESconnection()
	
	flag = 1
	count = 0
	while (flag==1):
		count +=1
		clear()
        #"incase of empty query"
        #"incase of random query"

		put_markdown(""" # QueRe""", strip_indent=10)
		query=input("Enter the query you want to search :",type="text")
		if(len(query)==0):
			while(len(query) == 0):
				query=input("Enter the query you want to search :",type="text")
		print("name :", query)
		# Text Output
		put_text("Query :", query)

		translated_query_to_english = translator.translate(query)
		translated_query_to_english = translated_query_to_english.text
		# Text Output
		put_text("Query in English :",translated_query_to_english)
		final_ids.clear()
		final_scores.clear()
		final1_score = []
		final1_id = []
		final2_score = []
		final2_id = []
		#keyword based searching
		res = keywordBasedSearching(es, translated_query_to_english)
		for hit in res['hits']['hits']:
			final1_score.append(hit['_score'])
			final1_id.append(hit['_id'])

		final1_score  = np.divide(final1_score, max(final1_score))
		final1_score = final1_score*0.3
		
		put_processbar('bar')
		for i in range(1, 21):
			set_processbar('bar', i / 20)
			time.sleep(0.1)
        	#semantic based searching
		
		processed_test_query = preprocessingQT(translated_query_to_english)
		sent_tfTensor = use_embeddings([processed_test_query])
		array_embeddings = tf.make_ndarray(tf.make_tensor_proto(sent_tfTensor))
		test_query_embeddings  = array_embeddings.tolist()
		final_list = calCosSim(test_query_embeddings, embeddings, idlist)
		for f in final_list:
			final2_score.append(float(f[0]))
			final2_id.append(f[1])

		print("k and s done")
		final2_score  = np.divide(final2_score, max(final2_score))
		final2_score = final2_score*0.7

		i = 0; j = 0
		count = 0
		while(i<len(final1_score) and j<len(final2_score)):
		  if(final2_score[j]>= final1_score[i]):
		    if len(final_ids)== 0 or not final2_id[j] in final_ids :
		      final_ids.append(final2_id[j])
		      final_scores.append(final2_score[j])
		      count +=1
		    j +=1
		  else:
		    if len(final_ids)== 0 or not final1_id[i] in final_ids:
		      final_ids.append(final1_id[i])
		      final_scores.append(final1_score[i])
		      count +=1
		    i +=1
		  if(count == 10):
		    break;

		while(count !=10 and i<len(final1_score)):
		  if  not final1_id[i] in final_ids:
		      final_ids.append(final1_id[i])
		      final_scores.append(final1_score[i])
		      count +=1

		while(count !=10 and j<len(final2_score)):
		  if  not final2_id[j] in final_ids:
		      final_ids.append(final2_id[j])
		      final_scores.append(final2_score[j])
		      count +=1
        # Table Output
		put_table([[final_scores[0], titledict[final_ids[0]], put_buttons([dict(label='View', value='p', color='light')],
		onclick=[showtext0])],
		[final_scores[1], titledict[final_ids[1]], put_buttons([dict(label='View', value='p', color='light')], onclick=[showtext1])],
		[final_scores[2], titledict[final_ids[2]], put_buttons([dict(label='View', value='p', color='light')], onclick=[showtext2])],
		[final_scores[3], titledict[final_ids[3]], put_buttons([dict(label='View', value='p', color='light')], onclick=[showtext3])],
		[final_scores[4], titledict[final_ids[4]], put_buttons([dict(label='View', value='p', color='light')], onclick=[showtext4])],
		[final_scores[5], titledict[final_ids[5]], put_buttons([dict(label='View', value='p', color='light')], onclick=[showtext5])],
		[final_scores[6], titledict[final_ids[6]], put_buttons([dict(label='View', value='p', color='light')], onclick=[showtext6])],
		[final_scores[7],titledict[final_ids[7]], put_buttons([dict(label='View', value='p', color='light')], onclick=[showtext7])],
		[final_scores[8], titledict[final_ids[8]], put_buttons([dict(label='View', value='p', color='light')], onclick=[showtext8])],
		[final_scores[9], titledict[final_ids[9]], put_buttons([dict(label='View', value='p', color='light')], onclick=[showtext9])]],
		header = ['Score', 'Related question from 10% stack Overflow dataset', 'Answers'])
			# Text Output
		put_text(" ~~~~~~~~~~~~~~~~~~~  Check related questions above for query no", count ,"~~~~~~~~~~~~~~~~~~~~~~~~")


		flag2 = radio("You wanna give feedback :", options=['yes', 'no'])
		print("flag2 :",flag2)
		if (flag2=="yes"):
			#flag2=1

			# Multi-line text input
			text = textarea('Feedback on our output if any', rows=3, placeholder='Some text')
			print("some text :",text)
		flag = radio("You wanna continue again :", options=['yes', 'no'])
		print("flag :", flag)

		
		if (flag=="yes"):
			flag = 1
		else:
			flag = 0
			clear()
			put_markdown(""" # ~~~~~~  Thanks for using our WEB APP ~~~~~~~""", strip_indent=10)
			exit(0)
			
			
if __name__=="__main__":
	server = start_server(app, port = 3000, debug = True)
	print("server:", server)
	
				
