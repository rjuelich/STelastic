from elasticsearch import Elasticsearch
import argparse
import os
import sys


parser = argparse.ArgumentParser(description="Returns Elasticsearch documents matching ticker query")
parser.add_argument("-i", "--index", required=True, help="name of ES index to query")
parser.add_argument("-t", "--ticker", required=True, help="Ticker to query")

args = parser.parse_args(sys.argv[1:])

dex = args.index
tick = args.ticker

client = Elasticsearch()

response = client.search(
	index= dex,
	body={
		"query": {
			"match" : {
				"tickers" : {
					"query" : tick
				}
			}
		}
	}
)


for hit in response['hits']['hits']:
	print(hit['_score'], hit['_source']['contentText'])


