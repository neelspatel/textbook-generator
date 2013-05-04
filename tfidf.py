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
import google
import pickle
from itertools import islice
from stemming.porter2 import stem


num_articles = 10

def error(string):
	#red and bold: \033[31m\033[1m \033[0m\033[0m
	return "\033[31m\033[1m" + string + "\033[0m\033[0m"

def get_tokens(query, src="google"):
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]

	if src == "wikipedia":
		print "Searching Wikipedia for " + query
		infile = opener.open('http://en.wikipedia.org/wiki/' + query)
		page = infile.read()
	else:
		print "Searching Google for " + query
		page = ""
		results = google.search(query, "com", "en", 1, 0, 1, 2.0)
		for result in results:
			print "on " + result
			page = google.get_page(result)
	
	#print page

	raw = nltk.clean_html(page) 

	#parses into tokens and saves as lwoercase
	tokens = map(lambda x:x.lower(),word_tokenize(raw))

	#removes punctuation and empty strings
	tokens = [s.translate(None, string.punctuation) for s in tokens]
	tokens = [s for s in tokens if s]

	return tokens

def load_idf():
	#tries to load in the pickle file from dictionary
	try:		
		idf_values = pickle.load(open ("idf.p", "rb"))
	except:
		#otherwise, loads in the idf values from a file
		print "Reading from file instead, and saving as pickle"
		idf_values = {}
		with open("idf.txt") as f:
			for line in f:
				(word, idf) = line.split()
				print "Word is '" + word + "', and idf is '" + idf + "'."
				idf_values[word] = idf
		pickle.dump(idf_values, open("idf.p", "wb"))

	return idf_values

def get_tf_idf(query, src="google"):
	tokens = get_tokens(query, src)

	#converts into a dictionary
	query_dictionary = Preprocess.list_to_dict(tokens,{})

	#print query_dictionary

	#creates a dictionary from a random wikipedia corpus
	#dictionary = Preprocess.get_corpus(num_articles)

	#loads in the dictionary of existing tf_idf words
	dictionary = load_idf()

	tf_idf_dictionary = {}

	#calculates the tfidf for each key, storing it in a new dictionary
	for key in query_dictionary.keys():
		tf = query_dictionary[key]
		if key in dictionary:
			idf = dictionary[key]
		else:
			idf = math.log(18,10)
		tf_idf_dictionary[key] = (float(tf)*float(idf))

	#print tf_idf_dictionary

	#sorts the dictionary based on the tfidf value, returning it as a list
	sorted_dictionary = sorted(tf_idf_dictionary.iteritems(), key=operator.itemgetter(1), reverse = True)

	return sorted_dictionary

#returns the top n words from a sorted list
def get_top_words(num, dictionary):	
	#words = [pair[0] for pair in dictionary]
	return dictionary[:num]

#removes any duplicates from a dictionary based on their stems
def remove_duplicates(dictionary):
	stems = []
	uniques = []
	for word in dictionary:
		root = stem(word)
		if not root in stems:
			stems.append(root)
			uniques.append(word)

	return uniques

def not_single(word):
	return len(word)!=1

#parses out the words that include punctuation from a sorted list
#also parses our single letter words
def parse(dictionary):
	words = [pair[0] for pair in dictionary]
	only_alpha =  filter(str.isalpha, words)
	only_non_single = filter(not_single, only_alpha)
	return only_non_single

