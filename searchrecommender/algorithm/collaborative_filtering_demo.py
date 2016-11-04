__author__ = 'saba.teserra'
#from searchrecommender.algorithm  import collaborative_filtering as cf
from math import log, exp
import re
import editdistance as distance
#from dicecore.textanalysis_pipeline.analysis_chains import skill_chain, title_chain
#from dicecore.textanalysis_pipeline.analyzers import analyze
from collections import defaultdict, Counter
import gensim
"""open preprocessed search logs and their statistics
 - instances for learning and decision making"""


#search_stream = open("searchrecommender/data/searches_by_id.txt", 'w')
#volume_stream = open("searchrecommender/data/search_volume_per_id", 'w')

searches ={}

with open("searchrecommender/data/searches_by_id1", 'rb') as f:
    for line in f:
        #print line
        arr = line.strip().split('|')
        if len(arr) == 2:
           searches[arr[0]] =arr[1].split(';')

print "ello"

"""
domain_ids with a large volume of search.
A separate analysis showed that some ips or cookies
have very high volume search coming from a single spot.
Tests are made with or without those ids included in the data
"""

spam_keys = [key for key, value in searches.iteritems() if len(value) > 50]

#for key in spam_keys:
#    del searches[key]

multi_search ={}

for key, value in searches.iteritems():
    if len(value) > 1 and key not in spam_keys:
        multi_search[key] = value

#with open("searchrecommender/data/better.txt", 'r') as r:
#    better = Counter(map(lambda x: x.strip().lower(), r.readlines()))
with open("searchrecommender/data/search_terms_id2.txt", 'r') as r:
    search_volume = defaultdict(lambda : 1.0)
    for i in r:
        z = i.lower().split('\t')
        search_volume[z[0].strip()] += float(z[1])
with open("searchrecommender/data/search_terms_id2.txt", 'r') as r:
    with open("searchrecommender/data/suggestions19.txt", 'a') as w:
#        query = str(raw_input("Enter Query: ")).strip().lower()
#        model = gensim.models.Word2Vec.load('/Users/rohan.bisariya/Desktop/IndustryC/jobModel')
        model = gensim.models.Word2Vec.load('/Users/rohan.bisariya/Documents/analytics-python-search-recommender/vectorModel')
        vocab = set(model.vocab)
        counter = 0
        notty = 0
        for line in r:
            suggestions = defaultdict(lambda : 0)
            counter += 1
            if counter%100==0: print counter
            a = line.split('\t')
#            if int(a[1]) > 3 : continue
            if int(a[1]) < 2 : break
            query = a[0].strip().lower()
            if len(query) < 2: continue
#            if query == "quit": break
#            veca = [x[1] for x in lsi_stem2[corp_stem.dictionary.doc2bow(map(stemmer.stem,query.lower().split()))]]
            for key, value in multi_search.iteritems():
                if query in value:
#                    if key in spam_keys
                    for keyword in value:
                        if keyword == query or len(keyword) < 2:
                            continue
#                        if False in map(lambda x : x in corp_stem.dictionary.values(), keyword.split()):
#                            notty+=1
#                            continue
#                        vecb = [x[1] for x in lsi_stem2[corp_stem.dictionary.doc2bow(map(stemmer.stem,keyword.lower().split()))]]
#                        if spatial.distance.cosine(veca, vecb) > 0.6: continue
                        if keyword.count(' ') > query.count(' ') + 3 or keyword.count(' ') > 6: continue
#                        if keyword in better: continue
                        suggestions[keyword] += 1
#                            suggestions[keyword] += 1 #+ log(1+ log(better[keyword]))
#            print len(suggestions)
            weighted_keys = {}
            query_s = set(query.split())
            if not query_s < vocab: continue
            for key, value in suggestions.iteritems():
                key_s = set(key.split())
                inter = key_s.intersection(query_s)
                if inter == key_s or inter == query_s
                if not key_s < vocab: continue
                if 'or' in key_s or 'and' in key_s or '/' in key: continue
                if 'jr.' in key_s or 'jr' in key_s or 'junior' in key: continue
                if 'sr.' in key_s or 'sr' in key_s or 'senior' in key: continue
                if 'entry level' in key or 'fresher' in key or 'remote' in key or 'part time' in key: continue
                if model.n_similarity(query_s, key_s) < 0.6: continue
                if value > 1:
                    if query_s < key_s and query == key[:len(query)]:
#                        if key in better:
#                            weighted_keys[key] = value * exp(1/distance.eval(key, query))*17
#                        else:
                        weighted_keys[key] = float(value) #* exp(1.0/distance.eval(key, query))*1
                    elif  query_s < key_s and query != key[:len(query)]:
#                        if key in better:
#                            weighted_keys[key] = value * exp(1/distance.eval(key, query))*15
#                        else:
                        weighted_keys[key] = float(value) #* exp(1.0/distance.eval(key, query))*1
                    else:
#                        if key in better:
#                            weighted_keys[key] = value * exp(1/distance.eval(key, query))*2
#                        else:
                        weighted_keys[key] = float(value) #* exp(1.0/distance.eval(key, query))
#                       (1/log(search_volume[key] + 1))* log((pmi[query][key]+0.0001)*1.0/float(search_volume[query]))
#                    weighted_keys[key] *= exp(model.n_similarity(query.split(), key.split()))*(key.count(' ') + 1.0)/(query.count(' ') + 1.0)
                    weighted_keys[key] *= exp(model.n_similarity(query_s, key_s))*(key.count(' ') + 1.0)/(query.count(' ') + 1.0)
            count = 0
            done = defaultdict(lambda : 0)
            done[frozenset(query.split())] = 1
            w.write('query= ' + query + '\n')
            for key, value in sorted(weighted_keys.iteritems(), key=lambda (k,v): (v,k),reverse=True):
                if count < 15:
                    if done[frozenset(key.split())] : continue
#                    if model.n_similarity(query.split(), key.split()) < 0.6: continue
                    done[frozenset(key.split())] = 1
                    w.write(key + '\t' + str(value)+'\n')
                    count += 1
#            if count < 15:
#                for key, value in sorted(weighted_keys.iteritems(), key=lambda (k,v): (v,k),reverse=True):
#                    if count < 15:
#                        if done[frozenset(key.split())] : continue
#                        done[frozenset(key.split())] = 1
#                        w.write(key + '\t' + str(value)+'\n')
#                        count += 1

#        print count

"""
with open("searchrecommender/data/search_terms.txt", 'r') as r:
#        query = str(raw_input("Enter Query: ")).strip().lower()
    counter = 0
    for line in r:
        counter += 1
        if counter%10000==0: print counter
        a = line.split('\t')
        if int(a[1]) < 100: break
with open("searchrecommender/data/better_searches.txt", 'w') as w:
#        query = str(raw_input("Enter Query: ")).strip().lower()
    reg2 = re.compile('title:\(|\)|\(|\"')
    counter = 0
    for line in list(l):
        w.write(str(line)+'\n')

import re
import collections
with open('searchrecommender/data/mono.txt', 'w') as w:
    pattern = "[^a-zA-Z]"
    frequencies = collections.Counter([re.sub(pattern, "", word.strip()) for line in searches for word in line.split()])
    for key, value in sorted(frequencies.iteritems(), key=lambda (k,v): (v,k),reverse=True):
        w.write(key +'\n')
with open('searchrecommender/data/search_terms_id2.txt', 'r') as r:
    total = 0
    pop = 0
    for l in r:
        i = l.split('\t')
        if len(i) < 2: continue
        x =  int(i[1])
        total += x
        if x < 10: continue
        pop += x

import re
from HTMLParser import HTMLParser
import urllib
import requests
import json
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk import word_tokenize
from collections import defaultdict, Counter
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline
from scipy import spatial
stop_words = stopwords.words('english')
stemmer = nltk.stem.SnowballStemmer('english')
def compute_ngrams(tokens, max_len = None, min_len = 1):
    #Compute n-grams of size min_len to max_len from tokens
    if max_len == None:
        max_len = len(tokens)
    if min_len > max_len:
        raise Exception("min_len cannot be more than max_len")
    ngrams = []
    for ngram_size in range(min_len, max_len + 1):
        for start in range(0, len(tokens) - ngram_size + 1):
            end = start + ngram_size -1
            words = []
            for i in range(start, end + 1):
                words.append(tokens[i])
            ngrams.append('_'.join(words))
    return ngrams
def process_row(row):

    row: row from pandas data frame with job posting information
    return : processed row with some textual features

#    if "sentences" not in row:
#        description = des.get_description(row["company"], row["xml"])
#        row["sentences"] = str(description)
    row["xml"] = row["sentences"]
    row["sentences"] = resolveHTML(strip_non_ascii(clean_str(row["sentences"])))
    row["tokenized"] = word_tokenize(row["sentences"])
    row["stemmed"] = map(stemmer.stem,row["tokenized"])
    return row
class MyHTMLParser(HTMLParser):
    p = []
    def handle_data(self, data):
        self.p.append(data)

def resolveHTML(s):
    parser = MyHTMLParser()
    parser.p = []
    parser.feed(s)
    parser.close()
    return ' '.join(xx for xx in parser.p)
def segment(job):
    #segment job xml into readable text
    job = re.sub("&nbsp;"," ",job)
    job = job.replace("&rsquo;", "'")
    job = job.replace("&amp;", "&")
    job = re.sub("So\\, |So ", "<br />So, ",job)
    job = re.sub(" +"," ",job)
    bigParts = re.split("\\|",job)
    descParts = re.split("</?HEAD>|</?TITLE>|</?BODY>|</?HTML>|</?[Hh]tml>|</?[Bb]ody>|</?[Tt]itle>|</?[Hh]ead>|"
        + "</?[Dd][ltd]>|</?D[LTD]>|</?[oO][lL]>|<br><br>|<[Bb][Rr]>|</?[Pp]>|</?[Ss]tyle>|</?[Mm]eta>|</?STYLE>|</?META>|"
        + "<span .*\"\">|<div .*>|</div>|</DIV>|</?[Ll][Ii]>|</?[Uu][Ll]>|<[bB][rR] />|<[bB][rR]/>|</?[hH][1-7]>|</?[Tt]able>|</?LINK>|</?[Ll]ink>|"
        + "</?TABLE>|</?[Tt]body>|</?[Tt]head>|</?[Tt]foot>|</?script>|</?SCRIPT>|</?noscript>|</?NOSCRIPT>|</?[tT][hrd]>|</?T[HRD]>|<hr />",
        bigParts[0])
    return ' '.join(descParts)


def strip_non_ascii(text):
    return ''.join(i for i in text if ord(i)<128)
map(stemmer.stem,
def clean_str(s):
    return re.sub("[,-]|\s+"," ",s.replace('"'," ").lower()).strip()
class MyCorpus(gensim.corpora.TextCorpus):
    def get_texts(self):
        count = 0
        for line in codecs.open(self.input, 'r' , 'utf-8'):
            count += 1
            if count%100000 == 0: print count
            line = line.split('\t')[1].lower()# for each relevant file
#            yield compute_ngrams(word_tokenize(segment(strip_non_ascii(line))), max_len=6, min_len=1)
            yield map(stemmer.stem,word_tokenize(segment(strip_non_ascii(line))))
with open('/Users/rohan.bisariya/Desktop/IndustryC/newJobsDirect.txt', 'r') as r:
    with open('/Users/rohan.bisariya/Desktop/IndustryC/sentences_words.txt', 'w') as w:
        count = 0
        for i in r:
            count += 1
            if count % 10000 == 0: print count
            w.write(' '.join(word_tokenize(segment(strip_non_ascii(i.strip())).lower())) + '\n')

"""
