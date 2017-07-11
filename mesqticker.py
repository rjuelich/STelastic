from datetime import datetime
import elasticsearch
from elasticsearch_dsl import Search
import os
import sys
import argparse
from elasticsearch import Elasticsearch
import configparser
import decimal
import json
import logging
import pprint
import time
import urllib

parser = argparse.ArgumentParser(description="Returns Elasticsearch documents matching ticker query")
parser.add_argument("-i", "--index", required=True, help="name of ES index to query")
parser.add_argument("-t", "--ticker", required=True, help="Ticker to query")

largs = parser.parse_args(sys.argv[1:])

dex = largs.index
tick = largs.ticker


client = Elasticsearch()

def getConfig():
	parser = argparse.ArgumentParser(description='Poll Quandl for dataset export status')
	parser.add_argument('--config-file', '-cf', dest='configFile', required=False, default='fields.config')
	parser.add_argument('--config-environment', '-env', dest='configEnv', required=False, default='dev')
        parser.add_argument("-i", "--index", required=True, dest='dex', help="name of ES index to query")
        parser.add_argument("-t", "--ticker", required=True, dest='tick', help="Ticker to query")
	args = parser.parse_args()
	cfg = configparser.ConfigParser()
	cfg.read(args.configFile)
	config = cfg[args.configEnv]
	fields = {x.strip() for x in config['rfields'].split(',')}
	config.fields = fields
	return config

def getTick(dex, tick):
    response = client.search(
        index = dex,
        body = {"query":{"multi_match":{"query":tick,"fields":"_all"}}}
    )
    config = getConfig()
    for hit in response['hits']['hits']:
        out = [str(hit['_score'])]
        for field in config.fields:
            out.append(str(hit['_source'][field]))
    
        print(out)


def main():
    getTick(dex, tick)

main()


    



'''
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
'''
