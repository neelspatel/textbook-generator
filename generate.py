#!/usr/bin/python

import tfidf
import process
import google
import pickle

#defines a term to search for
term = "biology"

#gets the list of all words with associated tf-idf scores
words = tfidf.get_tf_idf(term, "wikipedia")

#gets the cleaned list after removing list elements with non-alphanumeric charachters
cleaned = tfidf.parse(words)
cleaned = tfidf.remove_duplicates(cleaned)

#gets the list of top words (keywords)
keywords = tfidf.get_top_words(10, cleaned)

#gets all combinations of the keywords; this is a list of tuples
combinations = process.get_combinations(keywords)

try:		
	urls = pickle.load(open ("urls.p", "rb"))
except:
	#otherwise, creates and searches for the keywords
	print "Searching for each keyword set instead, and saving as pickle"
	urls = []
	for (word1, word2) in combinations:	
		print "Searching for " + word1 + ", " + word2 + "."
		try:
			results = google.search(term + " " + word1 + " " + word2, "com", "en", 1, 0, 3, 2.0)  			
			urls.append(results.next())
			urls.append(results.next())
			urls.append(results.next())

		except:
			print "HTML request overload."
			break

	pickle.dump(urls, open("urls.p", "wb"))

try:
	url_text_dictionary = pickle.load(open("url_text_dictionary.p", "rb"))
except:	
	url_text_dictionary = process.get_text_dictionary(urls)
	pickle.dump(urls, open("url_text_dictionary.p", "wb"))

#print url_text_dictionary

#now that we have the entire dictionary of url:text mappings, we can analyze instead
wiki_text = process.get_text('http://en.wikipedia.org/wiki/' + term)

