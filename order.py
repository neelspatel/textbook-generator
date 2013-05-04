import nltk
import math

# get summaribility score
def get_difference(wiki_dist, cur_dist):
  dist = 0.0
  for key in wiki_dist.keys():
    cur_dist += wiki_dist[key] - cur_dist[key]
    dist += math.pow(cur_dist, 2)
  return dist

# get orderability score
def get_order(cur_dist, order_keywords):
  order_score = 0.0
  for i in range(len(order_keywords)):
    order_score += i * cur_dist[order_keywords[i]]
  return order_score
