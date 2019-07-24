from collections import Counter
import pandas as pd
import csv
import operator
import collections
from WordsSets.SexismRacismTrumpWords import *


datasets_path = '../data-sets/'
file_name_prefix = 'clean_no_stop_words_'

games_list = {
    'fortnite': pd.read_csv(datasets_path + file_name_prefix + 'fortnite.csv'),
    'pubg': pd.read_csv(datasets_path + file_name_prefix + 'pubg.csv'),
    'fifa': pd.read_csv(datasets_path + file_name_prefix + 'fifa.csv'),
    'minecraft': pd.read_csv(datasets_path + file_name_prefix + 'minecraft.csv'),
    'bloodstained': pd.read_csv(datasets_path + file_name_prefix + 'bloodstained.csv'),
    'lol': pd.read_csv(datasets_path + file_name_prefix + 'lol.csv'),
    'overwatch': pd.read_csv(datasets_path + file_name_prefix + 'overwatch.csv'),
    'sims': pd.read_csv(datasets_path + file_name_prefix + 'sims.csv'),
    'wow': pd.read_csv(datasets_path + file_name_prefix + 'wow.csv'),
    'dota2': pd.read_csv(datasets_path + file_name_prefix + 'dota2.csv'),
}

for game_name, game_df in games_list.items():
    row_list = game_df.values.tolist()
    words_list = []

    for row in row_list:
        if type(row[0]) is str:
            _list = row[0].split()
            words_list.extend(_list)

    c = Counter(words_list)
    total_num_of_words = sum(c.values())
    dict_pair = dict(c)
    sorted_x = sorted(dict_pair.items(), key=operator.itemgetter(1), reverse=True)
    dict_pair = collections.OrderedDict(sorted_x)

    with open(datasets_path + '/bag_of_words/negative_words_freq_' + game_name, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for word, apperence_num in dict_pair.items():
            for attribute, neg_words in lists_of_negative_words.items():
                if word in neg_words:
                    writer.writerow([word, apperence_num, apperence_num / total_num_of_words])
                    break

    print("Finished calculating frequent words for the game : " + game_name)
