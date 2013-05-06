import nltk
import math

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
  wiki_keywords = filter (lambda x: x in keywords, wiki_words)
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
