__author__ = 'saba.teserra'
from searchrecommender.algorithm  import collaborative_filtering as cf
from math import log, exp
import re
import editdistance as distance

"""open preprocessed search logs and their statistics
 - instances for learning and decision making"""


search_stream = open("../data/searches_by_id.txt", 'w')
volume_stream = open("../data/search_volume_per_id", 'w')

searches ={}

with open("../data/searches_by_id.txt", 'rb') as f:
    for line in f.readlines():
        print line
        arr = line.strip().split('|')
        if len(arr) == 2:
           searches[arr[0]] =arr[1].split(',')



"""
domain_ids with a large volume of search.
A separate analysis showed that some ips or cookies
have very high volume search coming from a single spot.
Tests are made with or without those ids included in the data
"""

spam_keys = ["2f0424a44d84f52e", "90a9644bcceb2d39", "19b16ab8e3fc57bb", "1cf926e60e5ffb85"]

#for key in spam_keys:
#    del searches[key]

multi_search ={}

for key, value in searches.iteritems():
    if len(value) > 1:
        multi_search[key] = value


suggestions = {}
input = 'data scientist'
for key, value in multi_search.iteritems():
    if input in value:
        for keyword in value:
            if keyword == input:
                continue
            if keyword not in suggestions.keys():
                suggestions[keyword] = 1
            else:
                freq = suggestions[keyword]
                freq += 1
                suggestions[keyword] = freq


weighted_keys = {}

for key, value in suggestions.iteritems():
    if value > 1:
        if input in key and input == key[:len(input)]:
            weighted_keys[key] = value * exp(1/distance.eval(key, input))*15
        elif  input in key and input != key[:len(input)]:
            weighted_keys[key] = value * exp(1/distance.eval(key, input))*5
        else:
            weighted_keys[key] = value * exp(1/distance.eval(key, input))



count = 0


for key, value in sorted(weighted_keys.iteritems(), key=lambda (k,v): (v,k),reverse=True):
    if count < 15:
        print key, value
        count += 1

