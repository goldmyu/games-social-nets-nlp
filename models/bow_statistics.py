from collections import Counter
import pandas as pd
import operator
import collections
from WordsSets.SexismRacismTrumpWords import *


datasets_path = '../data-sets/'
file_name_prefix = 'clean_no_stop_words_'
properties = ['sexism', 'racism', 'trump-hate']


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
df_statistics = pd.DataFrame(columns=['game', 'property', 'sum-appear','percentage'])
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



    df_trump_neutral = pd.DataFrame(columns=['word', 'appereance', 'percentage'])
    for word, apperence_num in dict_pair.items():
        neutral_trump_words = lists_of_neutral_words.get("trump-hate_neutral_words")
        if word in neutral_trump_words:
            df_trump_neutral = df_trump_neutral.append({'word' : word , 'appereance': apperence_num, 'percentage': apperence_num / total_num_of_words}, ignore_index = True)

    df_statistics = df_statistics.append({'game': game_name, 'property' : 'neutral_trump', 'sum-appear' : df_trump_neutral.sum(axis=0)[1], 'percentage' : df_trump_neutral.sum(axis=0)[2]} , ignore_index=True)
    df_trump_neutral.to_csv(datasets_path + 'neutral_bow/neutral_trump_words_freq_' + game_name+".csv", index=False)

    for property in properties:
        df = pd.DataFrame(columns=['word', 'appereance', 'percentage'])
        for word, apperence_num in dict_pair.items():
            negative_words = lists_of_negative_words.get(property + '_words')
            if word in negative_words:
                df = df.append(
                    {'word': word, 'appereance': apperence_num, 'percentage': apperence_num / total_num_of_words},
                    ignore_index=True)

        df_statistics = df_statistics.append(
            {'game': game_name, 'property': property, 'sum-appear': df.sum(axis=0)[1],
             'percentage': df.sum(axis=0)[2]}, ignore_index=True)

        df.to_csv(datasets_path + 'negative_bow/negative_' + property +  '_words_freq_' + game_name + ".csv",index=False)

    print("Finished calculating frequent words for the game : " + game_name)
df_statistics.to_csv(datasets_path + 'bow_statistics.csv', index=False)
