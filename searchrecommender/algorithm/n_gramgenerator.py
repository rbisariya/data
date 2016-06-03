import io
import sys
import re
import stopwords_loader as sl
'''new_path = '/Users/saba.teserra/GitHub/new-python-analytics/analytics-python/ProfileSummarization'
if new_path not in sys.path:
    sys.path.append(new_path)
lis = ['this is text one','this is text an two with']
'''

#---------------------------------------------
#get monograms and their frequencies
def getmonogramfrequency(textlist, stopwords):
    monograms = {}
    for text in textlist:
        text = re.sub('[^A-Za-z0-9 ]+', '', text)
        terms = text.lower().split()
        for i in range (0, len(terms)):
            monogram = terms[i]
            if monogram in monograms:
                freq = monograms.get(monogram)
                freq+=1
                monograms[monogram] = freq
            else:
                if monogram not in stopwords:
                    monograms[monogram] = 1
    return monograms

#print getmonogramfrequency(lis)



#---------------------------------------------
#get bigrams and their frequencies
def getbigramfrequency(textlist, stopwords):
    bigrams = {}
    for text in textlist:
        text = re.sub('[^A-Za-z0-9 ]+', '', text)
        terms = text.lower().split()
        for i in range (0, len(terms)-1):
            pair = terms[i] +' ' + terms[i+1]
            if pair in bigrams:
                freq = bigrams.get(pair)
                freq+=1
                bigrams[pair] = freq
            else:
                if terms[i] not in stopwords and terms[i+1] not in stopwords:
                    bigrams[pair] = 1
    return bigrams
#print getbigramfrequency(lis)



#---------------------------------------------
#get trigrams and their frequencies
def gettrigramfrequency(textlist, stopwords):
    trigrams = {}
    for text in textlist:
        text = re.sub('[^A-Za-z0-9 ]+', '', text)
        terms = text.lower().split()
        for i in range (0, len(terms)-2):
            pair = terms[i] +' ' + terms[i+1] + ' ' + terms[i+2]
            if pair in trigrams:
                freq = trigrams.get(pair)
                freq+=1
                trigrams[pair] = freq
            else:
                if terms[i] not in stopwords and terms[i+1] not in stopwords and terms[i+2] not in stopwords:
                    trigrams[pair] = 1
    return trigrams
#print gettrigramfrequency(lis)


def get_skip_bigram (textlist, stopwords):
    skip_bigrams ={}
    for text in textlist:
        text = re.sub('[^A-Za-z0-9 ]+', '', text)
        terms = text.lower().split()
        if len(terms) < 3:
            continue
        for i in range (0, len(terms)-2):
            pair = terms[i] +' ' + terms[i+2]
            if pair in skip_bigrams:
                freq = skip_bigrams.get(pair)
                freq+=1
                skip_bigrams[pair] = freq
            else:
                if terms[i] not in stopwords and terms[i+2] not in stopwords:
                    skip_bigrams[pair] = 1
    return skip_bigrams
