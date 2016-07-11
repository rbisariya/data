__author__ = 'saba.teserra'

import ast
monogram_context = {}

bigram_context ={}
with open("../data/monogram_context.txt", 'rb') as f:
    for line in f.readlines():
        arr = line.strip().split('\t')
        monogram_context[arr[0]] = ast.literal_eval(arr[1])


with open("../data/bigram_context.txt", 'rb') as f:
    for line in f.readlines():
        arr = line.strip().split('\t')
        bigram_context[arr[0]] = ast.literal_eval(arr[1])


query = 'java'

arr = query.split()
last_term = arr[len(arr)-1]

context = monogram_context[last_term]

count = 0

two_level =[]
for key, value in sorted(context.iteritems(), key=lambda (k,v): (v,k),reverse=True):
    print query, key
    two_level.append(query + ' ' + key)
    count += 1
    if count > 5:
        break

count = 0
for val in two_level:
    if val in bigram_context.keys():
        bi_context = bigram_context[val]
        for key, value in sorted(bi_context.iteritems(), key=lambda (k,v): (v,k),reverse=True):
            print val, key
            count += 1
            if count > 5:
                break
