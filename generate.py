#!/usr/bin/python

import tfidf
import process
import google

#defines a term to search for
term = "biology"

#gets the list of all words with associated tf-idf scores
words = tfidf.get_tf_idf(term, "wikipedia")

#gets the cleaned list after removing list elements with non-alphanumeric charachters
cleaned = tfidf.parse(words)

#gets the list of top words (keywords)
keywords = tfidf.get_top_words(10, cleaned)

#gets all combinations of the keywords; this is a list of tuples
combinations = process.get_combinations(keywords)

urls = []

for (word1, word2) in combinations:	
	results = google.search(term + " " + word1 + " " + word2, "com", "en", 1, 0, 3, 2.0)         
    urls.append(list(results)[0])
    urls.append(list(results)[1])
    urls.append(list(results)[2])

print urls