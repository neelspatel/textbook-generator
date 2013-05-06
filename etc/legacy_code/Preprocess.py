#!/usr/bin/python
import nltk   
from urllib import urlopen
import urllib2
from cStringIO import StringIO
from tokenize import generate_tokens
import re
from nltk.tokenize import word_tokenize

#The purpose of this file is to get a corpus of texts for calculating tf-idf scores

#Chose text from wikipedia
#take the set of words in a text and compress it to a set of unique words
#For that set of unique words, add to the total dictionary of words


def unique_words (text):
	tokens = word_tokenize(text)

	lowered = map(lambda x:x.lower(),tokens)

	unique = []
	for i in lowered:
		if i not in unique:
			unique.append(i)

	return unique

def list_to_dict (list, dict):
	for word in list:
		word = str(word).strip()
		if word in dict:
			dict[word] = dict[word] + 1
		else:
			dict[word] = 1

	return dict

def get_corpus (num):
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]

	dictionary = {}

	#gets the corpus of wikipedia files
	for i in range(num):
		print "Processing article " + str(i)
		infile = opener.open('http://en.wikipedia.org/wiki/Special:Random')
		page = infile.read()
		raw = nltk.clean_html(page)  

		words = unique_words(raw)
		dictionary = list_to_dict(words, dictionary)
	return dictionary