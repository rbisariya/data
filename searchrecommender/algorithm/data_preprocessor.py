__author__ = 'saba.teserra'

import re
import searchrecommender.algorithm.n_gramgenerator as ng
import searchrecommender.algorithm.stopwords_loader as sl

source_file = "../data/job_search_cookies-10000.txt"

def get_search_terms(source_file):
    search_terms = []
    st_freq ={}
    ip = {}
    lines = []
    with open(source_file) as f:
        for raw_line in f.readlines():
            print raw_line
            raw_line = raw_line.strip()
            raw_line = re.sub(',', '', raw_line)

            str =raw_line.lower().split('|')

            if len(str) < 3:
                continue
            line =str[0]+'|'+str[2]
            if line in lines:
                continue
            lines.append(line)
            arr = line.split('|')
            term = arr[1].strip()
            if term != '':
                search_terms.append(term)
                if arr[0] in ip.keys():
                    ip[arr[0]].append(term)
                else:
                    ip[arr[0]] = [term]
                if term in st_freq.keys():
                    st_freq[term] += 1
                else:
                    st_freq[term] = 1
    return search_terms, st_freq, ip


search_terms, search_freq, ip = get_search_terms(source_file)

print "len", len(search_freq)


rare_terms =[]
for key, value in search_freq.iteritems():
    if value < 2:
        rare_terms.append(key)

print len(rare_terms)
for term in rare_terms:
    if term in search_freq.keys():
        del search_freq[term]




stopwordfile = "../data/stopwords.txt"
stopwords = sl.load_stopwords(stopwordfile)

skip_bigrams = ng.get_skip_bigram(search_terms, stopwords)
count = 0


monograms = ng.getmonogramfrequency(search_terms, stopwords)
bigrams = ng.getbigramfrequency(search_terms, stopwords)

trigrams = ng.gettrigramfrequency(search_terms, stopwords)

monogram_stream = open("../data/monograms.txt", "w")
skip_bigram_stream = open("../data/skip_bigrams.txt", "w")


bigram_stream = open("../data/bigrams.txt", "w")
trigram_stream = open("../data/trigrams.txt", "w")
search_terms_stream = open("../data/search_terms.txt", "w")

for key, value in monograms.iteritems():
    monogram_stream.write(key +'\t' + str(value)+'\n')


for key, value in bigrams.iteritems():
    bigram_stream.write(key +'\t' + str(value)+'\n')

for key, value in trigrams.iteritems():
    trigram_stream.write(key +'\t' + str(value)+'\n')

for key, value in search_freq.iteritems():
    search_terms_stream.write(key +'\t' + str(value)+'\n')
for key, value in skip_bigrams.iteritems():
    skip_bigram_stream.write(key +'\t' + str(value)+'\n')


monogram_stream.close()
bigram_stream.close()
trigram_stream.close()
search_terms_stream.close()
skip_bigram_stream.close()






