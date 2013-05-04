#!/usr/bin/python

import tfidf
import process
import google
import pickle
import order
import operator

#defines a term to search for
term = "Biology"

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
	urls = pickle.load(open ("dump/urls_" + term + ".p", "rb"))
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

	pickle.dump(urls, open("dump/urls_" + term + ".p", "wb"))


try:
	url_text_dictionary = pickle.load(open("dump/url_text_dictionary_" + term + ".p", "rb"))
except:	
	url_text_dictionary = process.get_text_dictionary(urls)
	pickle.dump(url_text_dictionary, open("dump/url_text_dictionary_" + term + ".p", "wb"))

#print url_text_dictionary

#now that we have the entire dictionary of url:text mappings, we can analyze instead
wiki_text = process.get_text('http://en.wikipedia.org/wiki/' + term)

#creates dictionaries for the summarability and order scores
ordered_keywords = order.get_ordered_keywords(wiki_text, keywords)
wiki_distribution = process.get_density(wiki_text, keywords)
summarability = {}
orderability = {}

#calculates the summarability score in a dictionary
for url, text in url_text_dictionary.iteritems():
	current_distribution = process.get_density(text,keywords)
	summarability[url] = order.get_difference(wiki_distribution, current_distribution)
	orderability[url] = order.get_order(current_distribution, ordered_keywords)

print summarability
print "\n\n"
print orderability

#gets the urls sorted by summarability as a list of (url, score) tuples
sorted_summarability = sorted(summarability.iteritems(), key=operator.itemgetter(1))
f = open('dump/sorted_summarability_' + term + ".txt",'w')
for (url, score) in sorted_summarability:
	try:
		f.write("  URL: " + url + "\n\n")
		text = url_text_dictionary[url]
		#print text
		f.write(text)
		f.write("\n\n")
	except:
		f.write("  URL: " + url + "\n\n")		
		f.write("Couldn't get text.")
		f.write("\n\n")

