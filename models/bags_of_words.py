# import nltk
# nltk.download()
import nltk
from nltk.tokenize import word_tokenize
import numpy as np
from collections import Counter
import pandas as pd
import csv
from pandas import DataFrame
import operator
from nltk.corpus import stopwords
import collections

game = 'wow'
DATA_SETS_PATH = '../data-sets/'
name_file = 'clean_no_stop_words_'+game+'.csv'
data = pd.read_csv(DATA_SETS_PATH+name_file)
df = DataFrame(data)
row_list = df.values.tolist()
words_list = []

for row in (row_list):
    if type(row[0]) is str:
        list = row[0].split()
        words_list.extend(list)

c = Counter(words_list)
sum = sum(c.values())
dict_pair = dict(c)
sorted_x = sorted(dict_pair.items(), key=operator.itemgetter(1), reverse=True)
dict_pair = collections.OrderedDict(sorted_x)

with open(DATA_SETS_PATH+'Results/Frequents/'+name_file, 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in dict_pair.items():
       writer.writerow([key, value, value/sum])


print("f")
