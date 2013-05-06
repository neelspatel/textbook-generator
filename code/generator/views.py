# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render

import tfidf
import process
import google
import pickle
import order
import operator
import json

def error(string):
	#red and bold: \033[31m\033[1m \033[0m\033[0m
	return "\033[31m\033[1m" + string + "\033[0m\033[0m"

def iframe(request):
	return render(request, 'generator/iframe.html', ({}))


def index(request):
	if 'query' in request.GET:
		term = request.GET['query']
		#replaces spaces with underscores
		term = term.replace(" ", "_")
		print error("****THE TERM IS " + term)
	else:
		#defines a term to search for
		term = "Manifold"

	#gets the list of all words with associated tf-idf scores
	words = tfidf.get_tf_idf(term, "wikipedia")

	#gets the cleaned list after removing list elements with non-alphanumeric charachters
	cleaned = tfidf.parse(words)
	cleaned = tfidf.remove_duplicates(cleaned)

	#gets the list of top words (keywords)
	keywords = tfidf.get_top_words(10, cleaned)
	print error(str(keywords))

	#gets all combinations of the keywords; this is a list of tuples
	combinations = process.get_combinations(keywords)

	try:		
		urls = pickle.load(open ("generator/dump/urls_" + term + ".p", "rb"))
	except:
		#otherwise, creates and searches for the keywords
		print "Searching for each keyword set instead, and saving as pickle"
		urls = []
		for (word1, word2) in combinations:	
			print "Searching for " + word1 + ", " + word2 + "."
			try:
				results = google.search(term + " " + word1 + " " + word2, "com", "en", 1, 0, 3, 2.0)  			
				
				for i in range(3):
					next_result = results.next()
					if not next_result in urls:
						urls.append(next_result)

			except:
				print "HTML request overload."
				break

		pickle.dump(urls, open("generator/dump/urls_" + term + ".p", "wb"))	

	#gets the cleaned text for each url
	try:
		url_text_dictionary = pickle.load(open("generator/dump/url_text_dictionary_" + term + ".p", "rb"))
	except:	
		url_text_dictionary = process.get_text_dictionary(urls)
		pickle.dump(url_text_dictionary, open("generator/dump/url_text_dictionary_" + term + ".p", "wb"))

	urls = url_text_dictionary.keys()
	pickle.dump(urls, open("generator/dump/urls_" + term + ".p", "wb"))	

	#gets the titles for each url
	try:
		print error("Loading titles.")
		url_titles = pickle.load(open("generator/dump/url_titles_" + term + ".p", "rb"))
		print error("Loaded existing titles.")
	except:	
		print error("Getting titles.")
		url_titles = process.get_titles(urls)
		pickle.dump(url_titles, open("generator/dump/url_titles_" + term + ".p", "wb"))

	#print url_text_dictionary

	#now that we have the entire dictionary of url:text mappings, we can analyze instead
	wiki_text = process.get_text('http://en.wikipedia.org/wiki/' + term)

	#creates dictionaries for the summarability and order scores
	ordered_keywords = order.get_ordered_keywords(wiki_text, keywords)
	#print error(str(ordered_keywords))
	wiki_distribution = process.get_density(wiki_text, keywords)
	summarability = {}
	orderability = {}

	#calculates the summarability score in a dictionary
	for url, text in url_text_dictionary.iteritems():
		current_distribution = process.get_density(text,keywords)
		summarability[url] = order.get_difference(wiki_distribution, current_distribution)
		orderability[url] = order.get_order(current_distribution, ordered_keywords)

	#print summarability
	print "\n\n"
	#print orderability

	#gets the urls sorted by summarability as a list of (url, score) tuples
	sorted_summarability = sorted(summarability.iteritems(), key=operator.itemgetter(1))
	sorted_orderability = sorted(orderability.iteritems(), key=operator.itemgetter(1))
	
	combined = order.combine_summarability_and_orderability(sorted_summarability, orderability, url_titles)

	print "Titles: " + str(url_titles)
	with_titles = []
	#adds in the title to the tuple
	for (url, score) in combined:
		with_titles.append((url, score, url_titles[url]))

	return render(request, 'generator/index.html', ({'summarability': json.dumps(sorted_summarability), 'orderability': json.dumps(sorted_orderability), 'combined': json.dumps(combined), 'with_titles': json.dumps(with_titles)}))
