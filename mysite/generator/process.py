import Preprocess
import tfidf as tl
import google 
import string
import math
import sys
import nltk
from urllib import urlopen
import urllib2
import collections
from BeautifulSoup import BeautifulSoup
import lxml.html


#returns the text from a given URL
def get_text(url):
  opener = urllib2.build_opener()
  opener.addheaders = [('User-agent', 'Mozilla/5.0')]
  try:
    print "Getting text from " + url
    infile = opener.open(url)
    page = infile.read()
    raw = nltk.clean_html(page) 
    return raw
  except:
    print "Sorry, could not read from " + url

#takes in a list of URLs and returns a dictionary of url:text mappings
def get_text_dictionary(url_list):
  dictionary = {}
  for url in url_list:
    dictionary[url] = get_text(url)

  return dictionary

#takes in a list of URls and returns a dictionary of url:title mappings
def get_titles(url_list):
  dictionary = {}
  print "List is " + str(url_list)
  for url in url_list:
    print "On " + url
    try:
      page = lxml.html.parse(url)
      title =  page.find(".//title").text    

      #gets title element    
      dictionary[url] = title
    except:
      dictionary[url] = url
    #print "Title of " + url + " is " + dictionary[url]

  return dictionary

def get_combinations(input):
  final = []
  for i in range(len(input)):
    for j in range(len(input) -i - 1):
      final.append((input[i], input[i + j + 1]))
  return final

#gets the density of each keyword (number of occurences over total number of words)
#returns a dictionary of keyword as key, density as value
def get_density (text, keywords):
  try:
    words = text.split()  
    words = map(lambda x:x.lower(),words)
    freqs = collections.Counter(words)
    keyword_freqs = {}  
    total = 0
    for keyword in keywords:
      keyword_freqs[keyword] = freqs[keyword]
      total += freqs[keyword]

    #normalizes everything by dividing by the total number of keywords
    #for keyword in keyword_freqs:
      #keyword_freqs[keyword] = keyword_freqs[keyword]/total
  except:
    print "Couldn't get the text."
    keyword_freqs = {}

  return keyword_freqs

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

#print get_links("gazelle")

