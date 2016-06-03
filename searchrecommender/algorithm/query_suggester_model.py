__author__ = 'saba.teserra'

from searchrecommender.algorithm import ngram_context_generator as cg

monograms = {}
bigrams  = {}
trigrams = {}
skip_bigrams ={}
search_terms ={}
with open("../data/monograms.txt", 'rb') as f:
    for line in f.readlines():
        arr = line.strip().split('\t')
        monograms[arr[0]] = int(arr[1])

with open("../data/bigrams.txt", 'rb') as f:
    for line in f.readlines():
        arr = line.strip().split('\t')
        bigrams[arr[0]] = int(arr[1])

with open("../data/trigrams.txt", 'rb') as f:
    for line in f.readlines():
        arr = line.strip().split('\t')
        trigrams[arr[0]] = int(arr[1])

with open("../data/skip_bigrams.txt", 'rb') as f:
    for line in f.readlines():
        arr = line.strip().split('\t')
        skip_bigrams[arr[0]] = int(arr[1])

with open("../data/search_terms.txt", 'rb') as f:
    for line in f.readlines():
        arr = line.strip().split('\t')
        search_terms[arr[0]] = int(arr[1])

"""
bigram_context = cg.get_bigram_context(bigrams, search_terms.keys(),monograms)
print len (bigram_context)
for key, value in bigram_context.iteritems():
    print key, value
    break"""

print "anything"
print len(search_terms)
monogram_context = cg.get_monogram_context(search_terms.keys(),monograms)

print len(monogram_context), "**"

monogram_context_stream = open("../data/monogram_context.txt", "w")
for key, value in monogram_context.iteritems():
    monogram_context_stream.write(key +"\t" + str(value) +'\n')

monogram_context_stream.close()


bigram_context = cg.get_bigram_context(bigrams, search_terms.keys(),monograms)

print len(bigram_context), "**"

bigram_context_stream = open("../data/bigram_context.txt", "w")

for key, value in bigram_context.iteritems():
    bigram_context_stream.write(key +"\t" + str(value) +'\n')

bigram_context_stream.close()

