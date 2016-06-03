#loads stopwords into a list variable
import io

def load_stopwords(filename):
    stopwords =[]
    file = open(filename)
    for line in file.readlines():
        stopwords.append(line.strip())
    return stopwords

def load_role_signals(filename):
    role_signals =[]
    file = open(filename)
    for line in file.readlines():
        role_signals.append(line.strip())
    return role_signals

