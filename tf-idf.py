#!/usr/bin/python

import Preprocess
import os
import sys
from urllib import urlopen
import urllib2
from tokenize import generate_tokens
import nltk
from nltk.tokenize import word_tokenize
import operator
import math
import string

num_articles = 10

def error(string):
	#red and bold: \033[31m\033[1m \033[0m\033[0m
	return "\033[31m\033[1m" + string + "\033[0m\033[0m"

if len(sys.argv) != 2:
	print error("Correct usage is tf-idf <query>")
	exit(1)


def get_tokens(query):
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]

	infile = opener.open('http://en.wikipedia.org/wiki/' + query)
	page = infile.read()
	raw = nltk.clean_html(page) 

	#parses into tokens and saves as lwoercase
	tokens = map(lambda x:x.lower(),word_tokenize(raw))

	#removes punctuation and empty strings
	tokens = [s.translate(None, string.punctuation) for s in tokens]
	tokens = [s for s in tokens if s]

	return tokens

def get_tf_idf(query):
	tokens = get_tokens(query)

	#converts into a dictionary
	query_dictionary = Preprocess.list_to_dict(tokens,{})

	#creates a dictionary from a random wikipedia corpus
	dictionary = Preprocess.get_corpus(num_articles)

	tf_idf_dictionary = {}

	#calculates the tfidf for each key, storing it in a new dictionary
	for key in query_dictionary.keys():
		tf = query_dictionary[key]
		if key in dictionary:
			idf = math.log(num_articles / dictionary[key], 10)
		else:
			idf = math.log(num_articles, 10)
		tf_idf_dictionary[key] = (tf*idf)

	#sorts the dictionary based on the tfidf value, returning it
	sorted_dictionary = sorted(tf_idf_dictionary.iteritems(), key=operator.itemgetter(1), reverse = True)

	return sorted_dictionary


query = sys.argv[1]
sorted_dictionary = get_tf_idf(query)
print sorted_dictionary

