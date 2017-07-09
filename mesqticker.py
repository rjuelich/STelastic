from datetime import datetime
import elasticsearch
from elasticsearch_dsl import Search
import os
import sys
import argparse
from elasticsearch import Elasticsearch

parser = argparse.ArgumentParser(description="Returns Elasticsearch documents matching ticker query")
parser.add_argument("-i", "--index", required=True, help="name of ES index to query")
parser.add_argument("-t", "--ticker", required=True, help="Ticker to query")

args = parser.parse_args(sys.argv[1:])

dex = args.index
tick = args.ticker

client = Elasticsearch()

def gettick(dex, tick, *fields):
	for field in fields:
		response = client.search(
			index = dex,
			body = {"query":{"match":{field:{"query":tick}}}}
		)
		for hit in response['hits']['hits']:
			print(hit['_score'], hit['_source']['wordpressId'], hit['_source']['title'],hit['_source']['contentText'])
		return;
	return;
gettick(dex,tick,'contentText','tickers')
