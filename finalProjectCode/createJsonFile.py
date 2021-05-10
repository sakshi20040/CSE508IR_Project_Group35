import json
import time
import sys
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk



def ESconnection():
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if es.ping():
            print('connected to elastic search')
    else:
            print('not connected to elastic search')
            sys.exit()
    return es

def create_json_file(es):
    body = {"mappings": {
            "properties": {
               "question": {
                    "type": "text"
                },
             }
           }
         }
    json_file = es.indices.create(index = 'question_bank', ignore = 400, body = body)
    print(json.dumps(json_file,indent=4))




if __name__=="__main__":
    es = ESconnection()
    create_json_file(es)
