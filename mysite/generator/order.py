import nltk
import math
import itertools
import operator

# get unique elements of a list preserve order
def unique (lst):
  checked = []
  for el in lst:
    if el not in checked:
	  checked.append(el)
  return checked

# get the ordered list of the first time that each keyword appears
def get_ordered_keywords (wiki_text, keywords):  
  wiki_words = wiki_text.split()
  wiki_words = map(lambda x:x.lower(),wiki_words)
  #print wiki_words
  wiki_keywords = filter (lambda x: x in keywords, wiki_words)
  #print str(wiki_keywords)
  return unique(wiki_keywords)

# get summaribility score
def get_difference(wiki_dist, cur_dist):
  #print wiki_dist
  #print cur_dist
  dist = 0.0
  for key in wiki_dist.keys():  
    try:  
      dist += math.pow((wiki_dist[key] - cur_dist[key]), 2)
    except:
      dist += 0.0
  return dist

# get orderability score
def get_order(cur_dist, order_keywords):
  order_score = 0.0
  for i in range(len(order_keywords)):
    try:
      order_score += i * cur_dist[order_keywords[i]]
    except:
      order_score += 0.0
  return order_score

def combine_summarability_and_orderability(sorted_summarability, orderability_dict, titles_dict):
  list_of_groups = itertools.izip_longest(*(iter(sorted_summarability),) * 10)
  master = []
  for i in range(len(sorted_summarability)/10 + 1):
    try:
      current_group = list(list_of_groups.next())
      #print "Cur grp: " + str(current_group)
      #print "Order dict: " + str(orderability_dict)
      #current_sorted = sorted(current_group, key=orderability_dict[operator.itemgetter(0)])
      current_sorted = sorted(current_group, key=lambda tup: orderability_dict[tup[0]], reverse = True)
      #print "Cur sorted: " + str(current_sorted)
      master += current_sorted
    except:
      print "exception"
      #print master
      return filter(None,master)

  #returns the filtered list without any Nones in it
  #print master
  return filter(None,master)


