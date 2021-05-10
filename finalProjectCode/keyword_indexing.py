import json
import time
import sys
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import csv
import numpy


def ESconnection():
    es = Elasticsearch([{"host": "localhost", "port": 9200}])
    if es.ping():
            print("connected to elastic search")
    else:
            print("not connected to elastic search")
            sys.exit()
    return es

def indexing(es, path):
    with open(path, encoding = "latin1") as csvfile:
        readCsv = csv.reader(csvfile, delimiter=',' )
        count=0
        for row in readCsv:
            if (count == 500000):
                break
            count +=1
            print(count)
            question_id = row[0]
            question_text = row[5]
            q = {"question" : question_text}
            res = es.index(index="question_bank", id= question_id, body=q)
    print("indexing completed")

if __name__=="__main__":
    es = ESconnection()
    indexing(es, "Questions.csv")
