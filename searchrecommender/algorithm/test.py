__author__ = 'saba.teserra'
from math import exp
input = "java developer"
key1 = "java developer and j2ee"

key2 = ".net developer"

key3 = "java developers"
import editdistance as ed
print exp(1/ed.eval(input, key1))*2, exp(1/ed.eval(input, key2))*2, (1/ed.eval(input, key3))
print key1[:len(input)]
