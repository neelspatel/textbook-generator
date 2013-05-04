import nltk
import math

def get_difference(wiki_dist, cur_dist):
  dist = 0.0
  for key in wiki_dist.keys():
    cur_dist += wiki_dist[key] - cur_dist[key]
    dist += math.pow(cur_dist, 2)
  return dist
