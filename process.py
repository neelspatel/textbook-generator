#This module is no longer used; it was only used during development and with prior stages of our application

import Preprocess
import tfidf as tl
import google 
import string
import math
import sys
import nltk

#given a list of keywords, returns every possible pairing of two keywords
def get_combinations (input):
  final = []
  for i in range(len(input)):
    for j in range(len(input)-i-1):
      final.append((input[i], input[i+j+1]))
  return final

#gets the density of each keyword (number of occurences over total number of words)
#returns a dictionary of keyword as key, density as value
def get_density (text, keywords):
  length = len(text.split())
  freqs = Counter(text.split())
  final = {}  


# get the top 10 results from tfidf output
def get_top (keywords_tuple):
  top_words = []
  for keyword in keywords_tuple[:5]:
    top_words.append(keyword[0])
  return top_words

def unpackage (query):
  # get the sorted set of link tuples with tf-idf
  keywords_top = get_top(tl.get_tf_idf(query, "wikipedia"))
  #store the keyword tree as a dictionary, with key initial keyword and value sub_keywords
  keywords_dict = {}
  for keyword in keywords_top:
    all_sub = tl.get_tf_idf(keyword)
    keywords_dict[keyword] = get_top(all_sub)
  return keywords_dict  

# used to get links from google searches of 
def get_links (query):
  keywords_dict = unpackage(query)
  list_links = []
  for keyword in keywords_dict:
    sub_words = keywords_dict[keyword]
    for word in sub_words:
      print keyword +"/" + word + "/" + query
      results = google.search(keyword + " " + word + " " + query, "com", "en", 1, 0, 1, 2.0)   
      #list_links.append(((list(results)[0]), keyword +"/" + word + "/" + query))
      list_links.append(list(results)[0])

  return list_links

#print get_links("test")

