import pandas as pd
from gensim.models import Word2Vec
from textblob import TextBlob
from WordsSets.SexismRacismTrumpWords import *

# ==================================================================================================================

properties = ['sexism', 'racism', 'trump-hate']  # "Racism" or "Trump-hate"

alpha = 1 / 3
beta = 1 / 3
gamma = 1 / 3
num_of_similar_words = 15

datasets_path = '../data-sets/'
no_stop_words_prefix = 'clean_no_stop_words_'
clean_prefix = 'clean_'

# ==================================================================================================================


games_df = {
    'fortnite': pd.read_csv(datasets_path + clean_prefix + 'fortnite.csv'),
    'pubg': pd.read_csv(datasets_path + clean_prefix + 'pubg.csv'),
    'fifa': pd.read_csv(datasets_path + clean_prefix + 'fifa.csv'),
    'minecraft': pd.read_csv(datasets_path + clean_prefix + 'minecraft.csv'),
    'bloodstained': pd.read_csv(datasets_path + clean_prefix + 'bloodstained.csv'),
    'lol': pd.read_csv(datasets_path + clean_prefix + 'lol.csv'),
    'overwatch': pd.read_csv(datasets_path + clean_prefix + 'overwatch.csv'),
    'sims': pd.read_csv(datasets_path + clean_prefix + 'sims.csv'),
    'wow': pd.read_csv(datasets_path + clean_prefix + 'wow.csv'),
    'dota2': pd.read_csv(datasets_path + clean_prefix + 'dota2.csv'),
}

games_df_no_stopwords = {
    'fortnite': pd.read_csv(datasets_path + no_stop_words_prefix + 'fortnite.csv'),
    'pubg': pd.read_csv(datasets_path + no_stop_words_prefix + 'pubg.csv'),
    'fifa': pd.read_csv(datasets_path + no_stop_words_prefix + 'fifa.csv'),
    'minecraft': pd.read_csv(datasets_path + no_stop_words_prefix + 'minecraft.csv'),
    'bloodstained': pd.read_csv(datasets_path + no_stop_words_prefix + 'bloodstained.csv'),
    'lol': pd.read_csv(datasets_path + no_stop_words_prefix + 'lol.csv'),
    'overwatch': pd.read_csv(datasets_path + no_stop_words_prefix + 'overwatch.csv'),
    'sims': pd.read_csv(datasets_path + no_stop_words_prefix + 'sims.csv'),
    'wow': pd.read_csv(datasets_path + no_stop_words_prefix + 'wow.csv'),
    'dota2': pd.read_csv(datasets_path + no_stop_words_prefix + 'dota2.csv'),
}

games_embedding_models = {
    'fortnite': Word2Vec.load("../saved_embedding_models/fortnite.model"),
    'pubg': Word2Vec.load("../saved_embedding_models/pubg.model"),
    'fifa': Word2Vec.load("../saved_embedding_models/fifa.model"),
    'minecraft': Word2Vec.load("../saved_embedding_models/minecraft.model"),
    'bloodstained': Word2Vec.load("../saved_embedding_models/bloodstained.model"),
    'lol': Word2Vec.load("../saved_embedding_models/lol.model"),
    'overwatch': Word2Vec.load("../saved_embedding_models/overwatch.model"),
    'sims': Word2Vec.load("../saved_embedding_models/sims.model"),
    'wow': Word2Vec.load("../saved_embedding_models/wow.model"),
    'dota2': Word2Vec.load("../saved_embedding_models/dota2.model"),
}


# ==================================================================================================================


def calc_x_term_freq(game_df_no_stopwords, _property, property_negative_words):
    num_of_neg_posts = 0

    row_list = game_df_no_stopwords.values.tolist()
    for row in row_list:
        if type(row[0]) is str:
            _list = row[0].split()
            for word in _list:
                if word in property_negative_words:
                    num_of_neg_posts += 1
                    break
    return num_of_neg_posts / len(game_df_no_stopwords)


def calc_x_sentiment_analysis(_game_name, _property, property_neutral_words):
    num_of_posts = 0
    polarity = 0
    game_df = games_df.get(_game_name)
    row_list = game_df.values.tolist()

    for row in row_list:
        if type(row[0]) is str:
            testimonial = TextBlob(row[0])
            _list = row[0].split()
            for word in _list:
                if word in property_neutral_words:
                    num_of_posts += 1
                    polarity += testimonial.sentiment.polarity
                    break
    return polarity / num_of_posts


def calc_x_embedding(_game_name, _property, property_negative_words, property_neutral_words):
    game_model = games_embedding_models.get(_game_name)
    bad_words = lists_of_negative_words.get('bad_words')

    neg_counter = 0
    existing_neutral_words_in_vocab = 0
    for neutral_word in property_neutral_words:
        try:
            similarity_list = game_model.wv.most_similar(positive=neutral_word, topn=num_of_similar_words)
            existing_neutral_words_in_vocab += 1
            for word in similarity_list:
                if word[0] in property_negative_words or word[0] in bad_words:
                    neg_counter += 1 / num_of_similar_words
        except:
            print('the word {} dont exist in game {}'.format(neutral_word, _game_name))
    return neg_counter/existing_neutral_words_in_vocab


def main():
    for game_name, game_df_no_stopwords in games_df_no_stopwords.items():
        print("calculating NEM values for game {}".format(game_name))
        for _property in properties:
            property_neutral_words = lists_of_neutral_words.get(_property + "_neutral_words")
            property_negative_words = lists_of_negative_words.get(_property + "_words")

            x_embedding = calc_x_embedding(game_name, _property, property_negative_words, property_neutral_words)
            x_term_freq = calc_x_term_freq(game_df_no_stopwords, _property, property_negative_words)
            x_sent_analysis = calc_x_sentiment_analysis(game_name, _property, property_neutral_words)
            nem_value = alpha * x_term_freq + beta * x_sent_analysis + gamma * x_embedding
            print('for the game {}, NEM value of the property {} is {} - x_term_freq {} '
                  'x_sent_analysis {} x_embedding {}'.format(game_name, _property, nem_value,
                                                             x_term_freq, x_sent_analysis, x_embedding))


if __name__ == '__main__':
    main()