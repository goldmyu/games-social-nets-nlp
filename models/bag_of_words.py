from collections import Counter
import pandas as pd
import csv
import operator
import collections

game_name = 'pubg'
DATA_SETS_PATH = '../data-sets/cleaned-data-sets/'
name_file = 'clean_no_stop_words_' + game_name + '.csv'
df = pd.read_csv(DATA_SETS_PATH+name_file)
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


with open(DATA_SETS_PATH +'Results/Frequents_words_' + game_name, 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in dict_pair.items():
       writer.writerow([key, value, value/sum])


print("Finished calculating frequent words for the game : " + game_name)
